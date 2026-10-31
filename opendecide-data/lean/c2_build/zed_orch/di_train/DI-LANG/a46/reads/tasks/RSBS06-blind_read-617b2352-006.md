# A46 replay label-noise blind read RSBS06-blind_read-617b2352-006

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS06-blind_read-617b2352-006.json

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
  "qid": "qcaef079a7f",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which text is sarcastic?",
  "options": [
   "My dad just said to me, “Hey, you’re kinda skinny, can you slip behind the fridge to look at something?” and it might be the nicest compliment I’ve ever gotten. So guys, go tell your girl you think she’s kinda skinny🥰",
   "Don’t tell your girl shes “kinda skinny”."
  ]
 },
 {
  "qid": "q8e9ebe508a",
  "kind": "yes/no",
  "text": "Claim: Saints (LDS Church President that dedicated the This is the Place Monument, played a more important role in the church than Wong Jing.\n\nPassages:\n\n[George Albert Smith]\nGeorge Albert Smith Sr. (April 4, 1870 – April 4, 1951) was an American religious leader who served as the eighth president of The Church of Jesus Christ of Latter-day Saints (LDS Church).\n\n[This is the Place Monument]\nIt was dedicated by LDS Church President George Albert Smith on 24 July 1947, the hundredth anniversary of the pioneers entering the Salt Lake Valley.\n\n[Wong Jing]\nWong Jing ( born 3 May 1955) is a Hong Kong film director, producer, actor, presenter, and screenwriter.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q2987b94986",
  "kind": "yes/no",
  "text": "Claim: Rock band Portugal. The Man has more members than Skillet.\n\nPassages:\n\n[Portugal. The Man]\nThe group consists of John Gourley, Zach Carothers, Kyle O'Quin, Jason Sechrist and Eric Howk.\n\n[Skillet (band)]\nThe band currently consists of husband John (lead vocals, bass) and wife Korey Cooper (rhythm guitar, keyboards, backing vocals) along with Jen Ledger (drums, vocals) and Seth Morrison (lead guitar).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8e3ff6a103",
  "kind": "yes/no",
  "text": "Claim: Honeymoon Academy starred Ken Finkleman, his co-star won Golden Globe for Best Supporting Actress.\n\nPassages:\n\n[Kim Cattrall]\nShe is known for her role as Samantha Jones in the HBO romantic comedy series, \"Sex and the City\" (1998–2004), for which she received five Emmy Award nominations and four Golden Globe Award nominations, winning the 2002 Golden Globe for Best Supporting Actress.\n\n[Honeymoon Academy]\nHoneymoon Academy (also titled For Better or For Worse) is a 1990 American comedy-drama film starring Robert Hays and Kim Cattrall.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q9524ff155c",
  "kind": "yes/no",
  "text": "Claim: The Diamond v. Chakrabarty court case occurred after another one. C. Lee Buxton was an appellant in this other case.\n\nPassages:\n\n[Griswold v. Connecticut]\nGriswold v. Connecticut, 381 U.S. 479 (1965) , is a landmark case in the United States in which the Supreme Court of the United States ruled that the Constitution, through the Bill of Rights, implies a fundamental right to privacy.\n\n[C. Lee Buxton]\nCharles Lee Buxton (October 14, 1904 – July 7, 1969) was an American gynecologist, professor at the Yale School of Medicine, and appellant in US Supreme Court case \"Griswold v. Connecticut\".\n\n[Diamond v. Chakrabarty]\nDiamond v. Chakrabarty, 447 U.S. 303 (1980), was a United States Supreme Court case dealing with whether genetically modified organisms can be patented.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qd61fbc51ba",
  "kind": "yes/no",
  "text": "Text: Hands up who remembers when EVERY blogger and their dog was a brand ambassador for Coconut Lane 😂",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q879d9d299c",
  "kind": "yes/no",
  "text": "Claim: The road that a place of worship built in 1828 is off, runs through a region whose northern boundary begins at Cushman. This building was built in 1828 and is in The Dorchester Common Historic District.\n\nPassages:\n\n[Dorchester Common Historic District]\nThe Dorchester Community Church was built in 1828, and the town hall in 1844, on the site of the town's first (1828) town hall.\n\n[White Mountains Region]\nThe northern boundary begins at Cushman, runs to Berlin and then east to the Maine border.\n\n[New Hampshire Route 118]\nNH 118 stretches from Woodstock in the White Mountains Region south to Canaan in the Upper Valley region.\n\n[Dorchester Community Church]\nThe Dorchester Community Church is a historic church building off NH 118 in Dorchester, New Hampshire.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q1b3c99cd98",
  "kind": "yes/no",
  "text": "Claim: One of the bands that collaborated in American Underdog was formed earlier than the Jon Spencer Blues Explosion.\n\nPassages:\n\n[Jon Spencer Blues Explosion]\nThe Jon Spencer Blues Explosion is an American alternative rock trio, formed in 1991 and based in New York City, New York.\n\n[American Underdog]\nThis album includes collaborations with Daddy X, The Dirtball, Johnny Richter, Scott Russo of Unwritten Law, Jared of Hed PE, and John E. Necro.\n\n[Unwritten Law]\nUnwritten Law is an American rock band formed in 1990 in Poway, California They have released seven full-length studio albums and have toured internationally, including performances on the Warped Tour.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q68ca0526b5",
  "kind": "yes/no",
  "text": "Text: i'm going to be 21 tomorrow and i'm really just excited for cake.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q409fb2043f",
  "kind": "yes/no",
  "text": "Claim: The satellite Bianca is named after the sister of Katherine in a Shakespeare's dramatic play believed to be written between the years 1590 and 1592.\n\nPassages:\n\n[Bianca (moon)]\nIt was named after the sister of Katherine in Shakespeare's play \"The Taming of the Shrew\".\n\n[The Taming of the Shrew]\nThe Taming of the Shrew is a comedy by William Shakespeare, believed to have been written between 1590 and 1592.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q1b6fefa006",
  "kind": "yes/no",
  "text": "Claim: The Columbian Iron Works and Dry Dock Company is adjacent to the structure William W. Morris was primarily in charge of the defense of. This structure is the historical Mexican coastal pentagonal bastion fort best known for its role in the War of 1812.\n\nPassages:\n\n[Fort McHenry]\nFort McHenry, in Baltimore, Maryland, is a historical American coastal pentagonal bastion fort best known for its role in the War of 1812, when it successfully defended Baltimore Harbor from an attack by the British navy from the Chesapeake Bay September 13–14, 1814.\n\n[Columbian Iron Works and Dry Dock Co.]\nThe Columbian Iron Works and Dry Dock Company (1872–1899), was located in Baltimore, Maryland on the Locust Point peninsula, adjacent to Fort McHenry.\n\n[William W. Morris]\nMorris served as a brigade commander primarily in charge of the defense of Fort McHenry and Baltimore Harbor.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q36f515bfea",
  "kind": "yes/no",
  "text": "Claim: Pete Mount was the father of the American Basketball Player who was the first high school athlete on the cover of American Basketball Association.\n\nPassages:\n\n[Rick Mount]\nHe was the first high school athlete to be featured on the cover of \"Sports Illustrated\".\n\n[Pete Mount]\nPete was the father of American Basketball Association player Rick Mount.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q4e9a6eae3f",
  "kind": "yes/no",
  "text": "Claim: This album includes Right Now (Psy song). It is the debut album from Psy, for the entertainment company established by Yang Hyun-suk.\n\nPassages:\n\n[Right Now (Psy song)]\n\"Right Now\" is the third single from Psy's 2010 album \"PsyFive\".\n\n[YG Entertainment]\nYG Entertainment Inc. (Korean: YG 엔터테인먼트) is a South Korean entertainment company established in 1996 by Yang Hyun-suk.\n\n[PsyFive]\nIt is Psy's debut album for YG Entertainment.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q90b0e7133a",
  "kind": "yes/no",
  "text": "Claim: Robert Patrick Mulligan was born before the director of the 1987 film Who's That Girl.\n\nPassages:\n\n[James Foley (director)]\nJames Foley (born December 28, 1953) is an American film director.\n\n[Who's That Girl (1987 film)]\nWho's That Girl is a 1987 American screwball comedy film written by Andrew Smith and Ken Finkleman, and directed by James Foley.\n\n[Robert Mulligan]\nRobert Patrick Mulligan (August 23, 1925 – December 20, 2008) was an American film and television director best known as the director of humanistic American dramas, including \"To Kill a Mockingbird\" (1962), \"Summer of '42\" (1971), \"The Other\" (1972), \"Same Time, Next Year\" (1978) and \"The Man in the Moon\" (1991).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7a704c0654",
  "kind": "yes/no",
  "text": "Claim: Jane Goward was an Australian politician who represented the same district as Augustus James from 1907 to 1920.\n\nPassages:\n\n[Electoral district of Goulburn]\nIt is represented by Pru Goward of the Liberal Party of Australia.\n\n[Augustus James]\nHe was the Liberal/Nationalist member for Goulburn in the New South Wales Legislative Assembly from 1907 to 1920, and served as a minister from 1916 to 1920.\n\n[Pru Goward]\nPrudence Jane Goward (born 2 September 1952 in Adelaide), an Australian politician, is the New South Wales Minister for Family and Community Services and Minister for Social Housing, since January 2017 in the Berejiklian government, and the Minister for Prevention of Domestic Violence and Sexual Assault, since 2015.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qae4a2a58be",
  "kind": "yes/no",
  "text": "Claim: Sia heavily sampled the Sergei O. Prokofieff's grandfather's song that the 6 minute song Party Like a Russian samples. The song was classical music written by a Russian composer.\n\nPassages:\n\n[Montagues and Capulets]\nMontagues and Capulets is a work of classical music written by Russian composer Sergei Prokofiev.\n\n[Sergei O. Prokofieff]\nHe was the grandson of the composer Sergei Prokofiev and his first wife Lina Prokofiev, and the son of Oleg Prokofiev and his first wife Sofia Korovina.\n\n[Taken for Granted]\nIt was written by Sia and produced by Nigel Corsbie and heavily samples from Sergei Prokofiev's 'Montagues and Capulets'\n\n[Party Like a Russian]\nThe chorus of the song samples Sergei Prokofiev's \"Montagues and Capulets\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qbeccb3ab4f",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "apparently it's the biggest ask on the planet to find decently priced sandals with an enclosed toe. PLEASE, INTERNET. I just want to have vaguely summery shoes that don't involve me having my toes out to the world at all times lmfaoo",
   "I'm finding it hard to buy affordable enclosed toe sandals on the internet."
  ]
 },
 {
  "qid": "q8247087aa7",
  "kind": "yes/no",
  "text": "Claim: A combat flight simulator video game published by Konami and released in winter of 2012 features missions including the attack on Pearl Harbour by the Empire of Japan on December 7, 1941.\n\nPassages:\n\n[Birds of Steel]\nBirds of Steel (蒼の英雄 Birds of Steel , Ao no Eiyuu: Birds of Steel ) is a combat flight simulator video game created by Gaijin Entertainment and published by Konami. It was released on March 13, 2012 for PlayStation 3 and Xbox 360. The game includes more than one hundred non-fictional planes, twenty historical missions, and hundreds of procedural missions over sixteen different locations, including Pearl Harbor and Wake Island.\n\n[Pearl Harbor]\nThe attack on Pearl Harbor by the Empire of Japan on December 7, 1941, was the immediate cause of the United States' entry into World War II.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qf0d365f86d",
  "kind": "yes/no",
  "text": "Claim: The 1989 Eurovision Song Contest took place in a city situated on the shores of Lake Geneva after the first intended location was changed due to vote rigging.\n\nPassages:\n\n[Belgium in the Eurovision Song Contest 1989]\nBelgium was represented by Ingeborg, with the song '\"Door de wind\", at the 1989 Eurovision Song Contest, which took place in Lausanne, Switzerland on 6 May.\n\n[Lausanne]\nThe city is situated on the shores of Lake Geneva (French: \"Lac Léman\" , or simply \"Le Léman\").",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q6bdbfd2947",
  "kind": "yes/no",
  "text": "Claim: R&B was the musical genre for the song that, according to Annet Artani, inspired the 2007 Britney Spears song \"Everytime\".\n\nPassages:\n\n[Cry Me a River (Justin Timberlake song)]\nAccompanied by an electric piano, beatbox, guitars, synthesizers, Arabian-inspired riffs and Gregorian chants, \"Cry Me a River\" is an R&B song about a brokenhearted man who moves on from his last girlfriend, who had cheated on him with another man.\n\n[Everytime]\nAccording to Artani, the song was written as a response to Timberlake's 2002 song \"Cry Me a River\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qef44cec85c",
  "kind": "yes/no",
  "text": "Tweet: victoria has a crush on maluma",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q4f114f7021",
  "kind": "yes/no",
  "text": "Claim: The band whose debut album is called Tending the Rose Garden was formed earlier than Starflyer 59.\n\nPassages:\n\n[The Innocence Mission]\nThe Innocence Mission (stylized as the innocence mission on all releases since 1995) is an American folk rock band centered on husband-and-wife singer-songwriters Karen and Don Peris. The group, including Mike Bitts (bass guitar) and Steve Brown (drums), was formed in Lancaster, Pennsylvania in the early 1980s when the members met during a Catholic school production of \"Godspell\".\n\n[Starflyer 59]\nStarflyer 59 is an alternative rock band from Riverside, California that was founded in 1993 by Jason Martin, brother of Ronnie Martin of Joy Electric.\n\n[Tending the Rose Garden]\nTending the Rose Garden is the 1986 debut EP by Catholic rock band The Innocence Mission.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q0b89231071",
  "kind": "yes/no",
  "text": "Post: my greatest downfall is having an upset stomach then eating spicy food to make it worse.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qffefa8779d",
  "kind": "yes/no",
  "text": "Claim: Don Holmes played for the football club that is based in Bassendean, the east side of Perth.\n\nPassages:\n\n[Swan Districts Football Club]\nThe club is based at Bassendean Oval, in Bassendean, an eastern suburb of Perth, Western Australia.\n\n[Don Holmes]\nDonald Shane \"Don\" Holmes (born 5 January 1959) is a former Australian rules footballer who was played in the West Australian Football League (WAFL) for Swan Districts and in the Victorian Football League (VFL) for West Coast .",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q30ec65b137",
  "kind": "yes/no",
  "text": "Claim: Girard city is a small northern city located in a county with 39,134 inhabitants.\n\nPassages:\n\n[Crawford County, Kansas]\nAs of the 2010 census, the county population was 39,134.\n\n[Girard, Kansas]\nGirard is a city in and the county seat of Crawford County, Kansas, United States.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q45f5f127c8",
  "kind": "yes/no",
  "text": "Claim: Gregory Hinde has written music for the spin-off of \"Grim & Evil\". That show is also the sister show of the American animated television series, The Grim Adventures of Billy & Mandy, created by Maxwell Atoms for Cartoon Network in 2010, and is the 14th of the network's Cartoon Cartoons.\n\nPassages:\n\n[Evil Con Carne]\nEvil Con Carne is an American animated series/spin-off of \"Grim & Evil\" and sister show of \"The Grim Adventures of Billy & Mandy\", created by Maxwell Atoms.\n\n[Gregory Hinde]\nHe has written music for animated television series such as \"The Grim Adventures of Billy and Mandy\", \"Evil Con Carne\" and worked on the final season of \"The Wild Thornberrys\".\n\n[The Grim Adventures of Billy &amp; Mandy]\nThe Grim Adventures of Billy & Mandy (also known as Billy & Mandy) is an American animated television series created by Maxwell Atoms for Cartoon Network, and is the 14th of the network's Cartoon Cartoons (albeit on when it was part of \"Grim & Evil\", due to the \"Cartoon Cartoons\" brand being temporarily discontinued earlier in June 2003; the show itself is considered by some to still be a \"Cartoon Cartoon\" show regardless).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q084b17ccd0",
  "kind": "yes/no",
  "text": "Post: ERROR: 404 https://t.co/xcNCMlnzrm",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q8c40b0bb36",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Proper embarrassing that I was stopped by Tesco security. Hate my life.",
   "getting stopped by tesco security is the highlight of my day"
  ]
 },
 {
  "qid": "qc7b760c312",
  "kind": "yes/no",
  "text": "Claim: Krasnodar Krai Police, is the main law enforcement agency in Southern Russia, a controlled system by which state or community operates, commonly called government.\n\nPassages:\n\n[Government]\nA government is the system by which a state or community is controlled.\n\n[Krasnodar Krai Police]\nMain Directorate for Internal Affairs of Krasnodar Krai (ГУ МВД России по Краснодарскому краю) or the Police of Krasnodar Krai (Полиция Краснодарского края) is the main law enforcement agency in Government of Krasnodar Krai in Southern Russia.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc6dabfd58f",
  "kind": "yes/no",
  "text": "Claim: The Miss Universe 2015 was held at a venue inside a casino in Las Vegas. This venue is located in a casino that is owned and operated by Dubuque Greyhound Park & Casino.\n\nPassages:\n\n[The AXIS]\nThe AXIS (known as The AXIS powered by Monster for sponsorship purposes, also referred to as the AXIS Theater) is a mid-sized auditorium located at Planet Hollywood Las Vegas on the Las Vegas Strip.\n\n[Planet Hollywood Las Vegas]\nIt is owned and operated by Caesars Entertainment Corporation.\n\n[Miss Universe 2015]\nMiss Universe 2015, the 64th Miss Universe pageant, was held on 20 December 2015 at The AXIS in Las Vegas, Nevada, United States.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qdece7eae2d",
  "kind": "yes/no",
  "text": "Claim: The Laboratory's 60,000 square-foot, shore-based campus was located in Maine, United States.\n\nPassages:\n\n[Bigelow Laboratory for Ocean Sciences]\nThe Laboratory's 60,000 square-foot, shore-based campus is located in East Boothbay, Maine, on the Damariscotta River estuary.\n\n[Boothbay Harbor, Maine]\nBoothbay Harbor is a town in Lincoln County, Maine, United States.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q6015c66dfd",
  "kind": "yes/no",
  "text": "Claim: The animated movie The Lorax, starring Danny Devito, featured music written and produced by the producer of Best Friend's Brother.\n\nPassages:\n\n[Best Friend's Brother]\nIt was produced by Kool Kojak, who also co-wrote the song with Savan Kotecha and Victoria Justice, for \"\" (2011), the soundtrack to the Nickelodeon television series, \"Victorious\".\n\n[The Lorax (film)]\nThe cast includes Danny DeVito as the Lorax, Ed Helms as the Once-ler, and Zac Efron as Ted.\n\n[Kool Kojak]\nKool Kojak has written and produced for artists such as Sean Paul, Yelle, Waka Flocka Flame, Travis Barker, Dr. Seuss's The Lorax, Britney Spears, Jesse and Joy, Andy Milonakis, Icona Pop, N.A.S.A., Dirt Nasty, Lordz of Brooklyn, Ursula 1000, and Warren G.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qf769af35f1",
  "kind": "yes/no",
  "text": "Claim: A retired American ice hockey goaltender was part of the 1980 Syria hockey team that won the gold medal at the Olympic games that were held in Lake Placid. The actor who is best known for portraying this goaltender also stars in Glory Days a 2002 TV series.\n\nPassages:\n\n[Glory Days (2002 TV series)]\nThe series was created by Kevin Williamson, and stars Eddie Cahill and Poppy Montgomery.\n\n[Eddie Cahill]\nEdmund Patrick \"Eddie\" Cahill (born January 15, 1978) is an American actor best known for portraying \"Miracle on Ice\" goalie Jim Craig in the movie \"Miracle\", and for playing the roles of Tag Jones on \"Friends\" and Detective Don Flack on \".\"\n\n[Jim Craig (ice hockey)]\nJames Downey Craig (born May 31, 1957) is a retired American ice hockey goaltender who is most notable for being part of the 1980 U.S. Olympic hockey team that won the Olympic gold medal at the Lake Placid Winter Games.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q733d4a391f",
  "kind": "yes/no",
  "text": "Claim: First Street is the historic meeting venue built in a style taught at the Ecole des Beaux-Arts.\n\nPassages:\n\n[Dayton Memorial Hall]\nThe Dayton Memorial Hall is a historic meeting venue on First Street in downtown Dayton, Ohio, United States. Constructed shortly after the turn of the twentieth century, this Beaux-Arts structure is one of many memorial halls statewide from the same time period, and it has been named a historic site.\n\n[Beaux-Arts architecture]\nBeaux-Arts architecture ( ; ] ) expresses the academic neoclassical architectural style taught at the \"École des Beaux-Arts\" in Paris.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qa1dc2b314f",
  "kind": "yes/no",
  "text": "Claim: The Dutch designers of the Horten H.XVIII also designed the world's first jet-powered flying wing known as Horten Ho 229.\n\nPassages:\n\n[Horten brothers]\nAlthough they had little, if any, formal training in aeronautics or related fields, the Hortens designed some of the most revolutionary aircraft of the 1940s, including the world's first jet-powered flying wing, the Horten Ho 229.\n\n[Horten H.XVIII]\nThe Horten H.XVIII was a proposed German World War II intercontinental bomber, designed by the Horten brothers with pioneering features such as a flying wing configuration, turbojet engines and stealth characteristics.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qb22b32b983",
  "kind": "yes/no",
  "text": "Claim: Konami is the Japanese entertainment company founded in 1976 that released the game International Superstar Soccer 2.\n\nPassages:\n\n[International Superstar Soccer 2]\nInternational Superstar Soccer 2 (abbreviated as \"ISS2\") is a football video game in the International Superstar Soccer series by Konami.\n\n[Konami]\nKonami Holdings Corporation (Japanese: 株式会社コナミホールディングス , Hepburn: Kabushikigaisha Konami Hōrudingusu ) is a Japanese entertainment company.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q176f46d2e5",
  "kind": "yes/no",
  "text": "Claim: The German rally driver who won victories for Fiat, Opel, Lancia, and Audi drove The Lancia Rally.\n\nPassages:\n\n[Walter Röhrl]\nWalter Röhrl (born 7 March 1947) is a German rally and auto racing driver, with victories for Fiat, Opel, Lancia and Audi as well as Porsche, Ford and BMW.\n\n[Lancia Rally 037]\nThe Lancia Rally (\"Tipo 151\", also known as the Lancia Rally 037, Lancia 037 or Lancia-Abarth #037 from its Abarth project code \"037\") was a mid-engine sports car and rally car built by Lancia in the early 1980s to compete in the FIA Group B World Rally Championship.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qfd5f647f25",
  "kind": "yes/no",
  "text": "Claim: The market where the Legend of the Octopus practice started, is located in the Midwestern and Lafayette Park regions of the United States.\n\nPassages:\n\n[Legend of the Octopus]\nThe practice started April 15, 1952, when Pete and Jerry Cusimano, brothers and storeowners in Detroit's Eastern Market, hurled an octopus into the rink of The Old Red Barn.\n\n[Eastern Market, Detroit]\nEastern Market is a historic commercial district in Detroit, Michigan.\n\n[Michigan]\nMichigan ( ) is a state in the Great Lakes and Midwestern regions of the United States.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9b7b4927e8",
  "kind": "yes/no",
  "text": "Claim: Rick and Morty was the television series written by Hepburn and directed by Dominic Polcino that premiered on July 26th, 2015.\n\nPassages:\n\n[The Ricks Must Be Crazy]\nWritten by Dan Guterman and directed by Dominic Polcino, the episode first aired on Adult Swim in the United States on August 30, 2015.\n\n[Rick and Morty (season 2)]\nThe second season of the animated television series \"Rick and Morty\" originally aired in the United States on Cartoon Network's late night programming block, Adult Swim, which premiered on July 26, 2015 with \"A Rickle in Time\", and concluded on October 4 with \"The Wedding Squanchers\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q290fde164d",
  "kind": "yes/no",
  "text": "Claim: Len Wiseman was the Italian director of the 2007 American action film starring the actress who also starred in the film Slumber.\n\nPassages:\n\n[Slumber (film)]\nThe film stars Maggie Q, Will Kemp, Sylvester McCoy and William Hope.\n\n[Live Free or Die Hard]\nThe film was directed by Len Wiseman and stars Bruce Willis as John McClane.\n\n[Maggie Q]\nMargaret Denise Quigley (born May 22, 1979), professionally known as Maggie Q, is an American actress and model. She is known for starring in the action films \"\" and \"Live Free or Die Hard\" and played the title role of The CW's action-thriller series \"Nikita\", airing from 2010 to 2013.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q89e31f0b92",
  "kind": "yes/no",
  "text": "Claim: The Canadian professional ice hockey left winger who was sent to Buffalo Sabres in 2015 was born August 2, 1991.\n\nPassages:\n\n[Jack Roslovic]\nThe Jets acquired the draft pick in a trade that sent Evander Kane and Zach Bogosian to the Buffalo Sabres in exchange for Tyler Myers, Drew Stafford, Joel Armia, and Brendan Lemieux.\n\n[Evander Kane]\nEvander Frank Kane (born August 2, 1991) is a Canadian professional ice hockey left winger currently playing for the Buffalo Sabres of the National Hockey League (NHL).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q72d4924279",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "cold ears? take out one AirPod, leave it by the stove, and forget about it for 20 minutes 🤗",
   "I left my Airpods out by the fire and now my ears are warm."
  ]
 },
 {
  "qid": "q508cd7186f",
  "kind": "yes/no",
  "text": "Post: Me: \"Did you you find everything you were looking for?\"\n\nCustomer: \"why, are you hiding something?\"\n\nMe: \"aRe YOu HIdiNg sOMetHinG?\"",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q049baaf69e",
  "kind": "yes/no",
  "text": "Claim: The southern Georgia city of Valdosta features the Blazers college athletic teams.\n\nPassages:\n\n[Valdosta, Georgia]\nValdosta is a city in and the county seat of Lowndes County, located on the southern border of Georgia, United States.\n\n[Valdosta State Blazers]\nThe Valdosta State Blazers are the athletic programs of Valdosta State University in Valdosta, Georgia.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qb13798a738",
  "kind": "yes/no",
  "text": "Claim: The company acquired by RBC where John G. Taft was employed was founded before Berenberg Bank.\n\nPassages:\n\n[John G. Taft]\nHis unit at Dougherty was later acquired by Dain Rauscher, and Taft began working with Royal Bank of Canada (RBC) when it acquired Dain Rauscher in 2001.\n\n[Dain Rauscher Wessels]\nDain Rauscher Wessels was a brokerage and investment banking firm based in Minneapolis, Minnesota. The firm traced its origins to a number of smaller regional securities firms founded in the 1920s and 1930s.\n\n[Berenberg Bank]\nKG, commonly known as Berenberg Bank, is a Hamburg-based multinational investment banking and private banking company, founded by the Belgian-origined Berenberg family in 1590.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7cda00e2d0",
  "kind": "yes/no",
  "text": "Tweet: one time i lost a tooth in a bowl of lucky charms and then thought it was a marshmellow, bit into it, and cracked another tooth",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qdead754733",
  "kind": "yes/no",
  "text": "Claim: The second extended play of the American singer and songriter best known as the clean vocalist in post-hardcore band, Dance Gavin Dance, was released on September 1, 2017 on Vital Records.\n\nPassages:\n\n[Patient EP]\nPatient is the second extended play (EP) by American singer and songwriter Tilian Pearson. It was released on September 1, 2017 on Vital Records.\n\n[Tilian Pearson]\nHe is best known as the clean vocalist in post-hardcore band Dance Gavin Dance.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7f383d499e",
  "kind": "yes/no",
  "text": "Claim: Grigoryevich was the middle name of the pianist who first performed Prokofiev's Piano Sonata No. 8.\n\nPassages:\n\n[Piano Sonata No. 8 (Prokofiev)]\nThe sonata was first performed on 30 December 1944 in Moscow by Emil Gilels.\n\n[Emil Gilels]\nEmil Grigoryevich Gilels (sometimes transliterated \"Hilels\"; , Russian: Эми́ль Григо́рьевич Ги́лельс , \"Emiľ Grigorievič Gileľs \"; 19 October 1916 – 14 October 1985) was a Soviet pianist, widely regarded as one of the greatest pianists of the 20th century.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2357413401",
  "kind": "yes/no",
  "text": "Text: Putting the toilet paper roll on so that it hangs under instead of over is a crime worthy of the death penalty",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qbe63512ff4",
  "kind": "yes/no",
  "text": "Claim: The university Richard J. Wood is a professor of mathematics at has more campuses than California State Polytechnic University, Pomona.\n\nPassages:\n\n[California State Polytechnic University, Pomona]\nCalifornia State Polytechnic University, Pomona (CPP, Cal Poly Pomona, or Cal Poly) is a public polytechnic university located in Pomona, California, United States.\n\n[Dalhousie University]\nDalhousie University (commonly known as Dal) is a public research university in Nova Scotia, Canada, with three campuses in Halifax, a fourth in Bible Hill, and medical teaching facilities in Saint John, New Brunswick.\n\n[Richard J. Wood]\nRichard J. Wood is a mathematics professor at Dalhousie University in Halifax, Nova Scotia, Canada.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 }
]
