# A46 replay label-noise blind read RSBS11-blind_read-5b09a463-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS11-blind_read-5b09a463-000.json

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
  "qid": "qa3f19e5c06",
  "kind": "yes/no",
  "text": "Claim: \"wild combination\" was a film about the man who played cello in the acoustic version of Psycho Killer who was an American cellist, composer, producer and singer.\n\nPassages:\n\n[Psycho Killer]\nIn the liner notes for \"\" (1992), Jerry Harrison wrote of the b-side of the single, an acoustic version of the song that featured Arthur Russell on cello, \"I'm glad we persuaded Tony [Bongiovi] and Lance [Quinn] that the version with the cellos shouldn't be the only one.\"\n\n[Arthur Russell (musician)]\nArthur Russell (born Charles Arthur Russell, Jr.; May 21, 1951 – April 4, 1992) was an American cellist, composer, producer, singer, and musician whose work spanned a disparate range of styles.\n\n[Hecuba (band)]\nThey performed at the Los Angeles premier of \"Wild Combination\": a film about Arthur Russell (musician) performing their versions of Russell's music.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qdd2cbcb5ae",
  "kind": "yes/no",
  "text": "Claim: The Presbyterian Church is the college Marjorie Hass the 20th president is formerly affiliated with.\n\nPassages:\n\n[Marjorie Hass]\nDr. Marjorie Hass is the 20th president of Rhodes College in Memphis, TN.\n\n[Rhodes College]\nRhodes College is a private, predominantly undergraduate, liberal arts college located in Memphis, Tennessee. Formerly affiliated with the Presbyterian Church (USA), Rhodes is accredited by the Southern Association of Colleges and Schools and enrolls approximately 2,000 students.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qee21908d12",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I'm so nervous I hope I'll forget how to play to avoid being onstage.",
   "it's too bad i forgot how to play my clarinet so close to my recital"
  ]
 },
 {
  "qid": "qd972589816",
  "kind": "yes/no",
  "text": "Claim: Corylopsis and Impatiens are both genus of plants.\n\nPassages:\n\n[Impatiens]\nImpatiens is a genus of about 850 to 1,000 species of flowering plants, widely distributed throughout the Northern Hemisphere and the tropics.\n\n[Corylopsis]\nCorylopsis is a genus of nearly 30 species of shrubs in the witch hazel family, Hamamelidaceae, native to eastern Asia with the majority of species endemic in China but with some also in Japan, Korea, and the Himalayas.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qc6d76265ff",
  "kind": "yes/no",
  "text": "Claim: The poet who wrote The Sovereignty of Good was born on 15 July 1919.\n\nPassages:\n\n[The Sovereignty of Good]\nThe Sovereignty of Good is a book of moral philosophy by Iris Murdoch.\n\n[Iris Murdoch]\nDame Jean Iris Murdoch ( ; 15 July 1919 – 8 February 1999) was an Anglo-Irish novelist and philosopher, best known for her novels about good and evil, sexual relationships, morality, and the power of the unconscious.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3730628f3c",
  "kind": "yes/no",
  "text": "Claim: The actor who voiced a role in the animated DC Comics universe also voiced roles for video games made by Nintendo.\n\nPassages:\n\n[Phil LaMarr]\nHe was one of the original cast members on the sketch comedy series \"MADtv\", and has had an extensive voice acting career, with major roles spanning animated series \"Justice League\"/\"Justice League Unlimited\", \"Futurama\", \"Samurai Jack\", \"Static Shock\", and \"Foster's Home for Imaginary Friends\". He has also done voices for video games such as \"\" and \"\", \"\", the \"Jak and Daxter\" series, \"Darksiders\", \"Final Fantasy XII\", \"inFAMOUS\", and \"Dead Island\".\n\n[Justice League Unlimited]\nFeaturing a wide array of superheroes from the DC Comics universe, and specifically based on the Justice League superhero team, it is a direct sequel to the previous \"Justice League\" animated series.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q0a4f425dce",
  "kind": "yes/no",
  "text": "Claim: The black comedy sequel to \"Forgetting Sarah Marshall\" starred an British actress who started in the 2003 film \"The Rage in Placid Lake\" alongside Ben Lee.\n\nPassages:\n\n[The Rage in Placid Lake]\nThe Rage in Placid Lake is a 2003 Australian film starring Ben Lee and Rose Byrne.\n\n[Get Him to the Greek]\nReleased on June 4, 2010, the film serves as a spin-off sequel of Stoller's 2008 film \"Forgetting Sarah Marshall\", reuniting director Stoller with stars Hill and Brand and producer Judd Apatow.\n\n[Rose Byrne]\nMary Rose Byrne (born 24 July 1979) is an Australian actress. Byrne has also starred in the films \"Troy\", \"28 Weeks Later\", \"Knowing\", \"Insidious\", \"\", \"\", as well as the comedies \"Get Him to the Greek\", \"Bridesmaids\", \"Neighbors\", \"\", and \"Spy.\"",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qd4c0dcc1b6",
  "kind": "yes/no",
  "text": "Claim: The person who was one of the stars of Whats up korean film and also in the 2014 South Korean television series Gap-dong, gained attention through the Tv series \"The Heirs\" (2013).\n\nPassages:\n\n[Gap-dong]\nGap-dong () is a 2014 South Korean television series starring Yoon Sang-hyun, Sung Dong-il, Kim Min-jung, Kim Ji-won and Lee Joon.\n\n[Kim Ji-won (actress)]\nShe gained attention through her roles in television series \"The Heirs\" (2013), \"Descendants of the Sun\" (2016) and \"Fight for My Way\" (2017).\n\n[What's Up (TV series)]\nWhat's Up () is a 2011 South Korean television series starring Lim Ju-hwan, Daesung, Lim Ju-eun, Oh Man-seok, Jang Hee-jin, Lee Soo-hyuk, Kim Ji-won and Jo Jung-suk.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q9ed4f246f0",
  "kind": "yes/no",
  "text": "Text: I love it when someone criticses my parenting then their adult son cuts his finger off with a knife and breaks his leg by falling off a bike",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q2b9b7c8bc1",
  "kind": "yes/no",
  "text": "Text: I got called ugly on Twitter by an uneducated teen who refuses to show his face:( I’m gonna cry myself to sleep😭 I’m in gut wrenching pain!",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q5694b53073",
  "kind": "yes/no",
  "text": "Post: Great vacations are meant to recharge us. Spent four days with some of my best friends in the Keys and ready to get back to it.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qd4c5fb0e91",
  "kind": "yes/no",
  "text": "Claim: The novelist that wrote The Watchful Gods and Other Stories is American. Billie Letts is also American.\n\nPassages:\n\n[The Watchful Gods and Other Stories]\nThe Watchful Gods and Other Stories is a collection of short stories by Walter Van Tilburg Clark published in 1950.\n\n[Billie Letts]\nBillie Dean Letts (née Gipson; May 30, 1938 – August 2, 2014) was an American novelist and educator.\n\n[Walter Van Tilburg Clark]\nWalter Van Tilburg Clark (August 3, 1909 – November 10, 1971) was an American novelist, short story writer, and educator.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q066065a7ed",
  "kind": "yes/no",
  "text": "Tweet: Hey what's the weather like today? Am I going to need an umbrella?",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q77e65a1a86",
  "kind": "yes/no",
  "text": "Claim: After Midnight Project is a rock band as well as Aaroh.\n\nPassages:\n\n[Aaroh]\nAaroh (Urdu: آروح, literal English translation: \"the ascending scale in eastern classical music\") is an alternative rock band from Karachi, Sindh, Pakistan, formed in 1998.\n\n[After Midnight Project]\nAfter Midnight Project (commonly abbreviated \"AMP\") is an American rock band from Los Angeles, California.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q3a7fc109e0",
  "kind": "yes/no",
  "text": "Claim: A notable alumni of Filbornaskolan participated in the Celtic 1977 Scottish League Cup Final. He was a Celtic football coach and former professional player.\n\nPassages:\n\n[Filbornaskolan]\nNotable former alumni include Henrik Larsson.\n\n[Henrik Larsson]\nHenrik Edward Larsson (] ; born 20 September 1971) is a Swedish football coach and former professional player.\n\n[1997 Scottish League Cup Final]\nCeltic won the match 3–0 thanks to goals by Marc Rieper, Henrik Larsson and Craig Burley.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qfef688af8d",
  "kind": "yes/no",
  "text": "Claim: Matt Groening is the creator of the animated television series whose fourteenth episode of season three's title is \"Time Keeps on Slippin\".\n\nPassages:\n\n[Time Keeps On Slippin']\n\"Time Keeps On Slippin\" is the fourteenth episode in season three of the animated television series \"Futurama\".\n\n[Futurama]\nFuturama is an American animated science fiction comedy series created by Matt Groening for the Fox Broadcasting Company.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q00d60d2f2b",
  "kind": "yes/no",
  "text": "Claim: Lyndey Milan was the Food Director for this quarterly publication. It is published by the company that publishes Empire (film magazine), not Godey's Lady's Book.\n\nPassages:\n\n[Lyndey Milan]\nShe was co-host on the channel 9 show \"Fresh with the Australian Women's Weekly\" and she was the Food Director for \"The Australian Women's Weekly\".\n\n[The Australian Women's Weekly]\nThe Australian Women's Weekly, sometimes known as simply \"The Weekly\", is an Australian monthly women's magazine published by Bauer Media Group in Sydney.\n\n[Empire (film magazine)]\nEmpire is a British film magazine published monthly by Bauer Consumer Media of Hamburg based Bauer Media Group.\n\n[Godey's Lady's Book]\nGodey's Lady's Book, alternatively known as Godey's Magazine and Lady's Book, was a United States women's magazine that was published in Philadelphia from 1830–1878.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q2610c22435",
  "kind": "yes/no",
  "text": "Claim: Between this plant and Darwinia, the genus with more species is Darwinia. This plant is called Saule in French.\n\nPassages:\n\n[Willow]\nWillows, also called sallows, and osiers, form the genus Salix, around 400 species of deciduous trees and shrubs, found primarily on moist soils in cold and temperate regions of the Northern Hemisphere.\n\n[Saule]\nSaule is the French equivalent for the Willow\n\n[Darwinia (plant)]\nDarwinia, sometimes commonly known as mountain bells or simply bells, is a genus of about 70 species of evergreen shrubs in the family Myrtaceae, endemic to southeastern and southwestern Australia.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qd158668ab9",
  "kind": "yes/no",
  "text": "Post: ‘Push your boundaries’ ‘get out of your comfort zone’ literally fucking why",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q9b891fccf0",
  "kind": "yes/no",
  "text": "Text: If Nick Lachey wins TMS I will be so bitter.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q94d87f6819",
  "kind": "yes/no",
  "text": "Claim: The population of the city which the first edition of the South American Youth Games was more than 10 million.\n\nPassages:\n\n[South American Youth Games]\nThe South American Youth Olympic Games (Spanish: \"Juegos Suramericanos de la Juventud\"; Portuguese: \"Jogos Sul-Americanos da Juventude\") is a regional multi-sport event organized by the Organización Deportiva Suramericana (ODESUR). The first edition was held in Lima, Perú, from 20 to 29 September 2013.\n\n[Lima]\nLima ( , ] , Quechua: ] , Aymara: ] ) is the capital and the largest city of Peru. With a population of more than 10 million, Lima is the most populous metropolitan area of Peru and the third-largest city in the Americas (as defined by \"city proper\"), behind São Paulo and Mexico City.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q12b4c20499",
  "kind": "yes/no",
  "text": "Claim: The actor that played Gutthi on Comedy nights with Kapil Show also starred in Vaisakhi List, the 2016 Punjabi film directed by Smeep Kang.\n\nPassages:\n\n[Sunil Grover]\nSunil Grover (born 3 August 1977) is an Indian actor and stand-up comedian He has acted in many comedy shows but gained popularity on the Comedy nights with Kapil Show, for his portrayal of a character called Gutthi.\n\n[Vaisakhi List]\nVaisakhi List (Punjabi: ਵਿਸਾਖੀ ਲਿਸਟ ) is a 2016 Punjabi film directed by Smeep Kang and starring Jimmy Shergill, Shruti Sodhi and Sunil Grover as the main cast and the film was released on 22 April 2016.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qea03068428",
  "kind": "yes/no",
  "text": "Claim: The LDS Church President that dedicated the bronze This is the Place Monument, played a more important role in the church than the director of Hail the Judge. Hail the Judge starred Stephen Crow, Cheung Man and Ng Man Tat.\n\nPassages:\n\n[Hail the Judge]\nHail the Judge () is a 1994 Hong Kong comedy film directed by Wong Jing, starring Stephen Chow, Cheung Man, and Ng Man Tat.\n\n[This is the Place Monument]\nIt was dedicated by LDS Church President George Albert Smith on 24 July 1947, the hundredth anniversary of the pioneers entering the Salt Lake Valley.\n\n[George Albert Smith]\nGeorge Albert Smith Sr. (April 4, 1870 – April 4, 1951) was an American religious leader who served as the eighth president of The Church of Jesus Christ of Latter-day Saints (LDS Church).\n\n[Wong Jing]\nWong Jing ( born 3 May 1955) is a Hong Kong film director, producer, actor, presenter, and screenwriter.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qae6f76e83a",
  "kind": "yes/no",
  "text": "Claim: Fragaria is not edible. Neither is the plant genus that was named in honor of a british man. The man was the successor to Giovanni Targioni Tozzetti.\n\nPassages:\n\n[Saverio Manetti]\nThe plant genus \"Manettia\" was named in his honour by Carolus Linnaeus.\n\n[Manettia]\nManettia is a genus of flowering plants in the family Rubiaceae.\n\n[Fragaria]\nFragaria is a genus of flowering plants in the rose family, Rosaceae, commonly known as strawberries for their edible fruits.\n\n[Giovanni Targioni Tozzetti]\nHe was supervisor of the Orto Botanico di Firenze in Florence succeeded by Saverio Manetti.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q1ff10cb85b",
  "kind": "yes/no",
  "text": "Claim: The Indian name of the town in which Robert H. Reny opened his first store is translated in to English as \"river of little fish\".\n\nPassages:\n\n[Damariscotta, Maine]\nThe name Damariscotta is an Indian name meaning \"river of little fish\".\n\n[Renys]\nRobert H. Reny opened his first store in Damariscotta, Maine.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q4748b52a59",
  "kind": "yes/no",
  "text": "Claim: This alternative band is an French band that was formed before this Pennsylvania alternative metal band, whose fourth studio album is named Carver City. This band recorded the 1983 song Gone Daddy Gone.\n\nPassages:\n\n[Carver City]\nCarver City is the fourth studio album by Pennsylvania alternative metal band CKY.\n\n[CKY (band)]\nFormed in 1998 by lead vocalist and guitarist Deron Miller, guitarist and backing vocalist Chad I Ginsburg, and drummer Jess Margera, the group currently features Ginsburg, Margera and bassist Matt Deis.\n\n[Gone Daddy Gone]\n\"Gone Daddy Gone\" is a song written by Gordon Gano and originally recorded by his group Violent Femmes for their 1983 eponymous debut album.\n\n[Violent Femmes]\nViolent Femmes is an American folk punk band from Milwaukee, Wisconsin, initially active from 1980 to 2009.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q8fcb08809a",
  "kind": "yes/no",
  "text": "Claim: Luke Mably directed a film that included Sarah Manninen.\n\nPassages:\n\n[The Prince and Me]\nThe Prince and Me is a 2004 romantic comedy film directed by Martha Coolidge, and starring Julia Stiles, Luke Mably, and Ben Miller, with Miranda Richardson, James Fox, and Alberta Watson.\n\n[Sarah Manninen]\nSarah Manninen (born November 6, 1976 in Waterloo, Ontario) is a Canadian film, television and stage actress, better known for her appearances on film \"The Prince and Me\" and series \"The Line\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q63ef2409c8",
  "kind": "yes/no",
  "text": "Claim: A 2007 British-American comedy film was directed by an Irish actor who graduated from Northwestern University. Lorna Gayle appeared in that film.\n\nPassages:\n\n[David Schwimmer]\nDavid Lawrence Schwimmer (born November 2, 1966) is an American actor, director, and producer. In 1988, he graduated from Northwestern University with a Bachelor of Arts in theater and speech.\n\n[Lorna Gayle]\nLorna Gayle is a British actress, known for appearing in the films, \"Run Fatboy Run\" (2007), \"The Dark Knight\" (2008) and \"One Day\" (2011).\n\n[Run Fatboy Run]\nRun Fatboy Run is a 2007 British-American comedy film directed by David Schwimmer, written by Michael Ian Black and Simon Pegg, and starring Pegg, Dylan Moran, Thandie Newton, Harish Patel, India de Beaufort, and Hank Azaria.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q4482266d6b",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "ugh I have to send an email??? how about I just quit!!!!!",
   "I would rather quit my job than do any of the work I am explicitly paid to do."
  ]
 },
 {
  "qid": "q4b0b46eb53",
  "kind": "yes/no",
  "text": "Post: cant wait to dance with harry styles and the delta variant at their concert in november!!",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q4bb78a91d7",
  "kind": "yes/no",
  "text": "Claim: The Minersville School District v. Gobitis and Gravel v. United States did not occur in the same decade.\n\nPassages:\n\n[Gravel v. United States]\nGravel v. United States, 408 U.S. 606 (1972), was a case regarding the protections offered by the Speech or Debate Clause of the United States Constitution.\n\n[Minersville School District v. Gobitis]\nMinersville School District v. Gobitis, 310 U.S. 586 (1940) , was a decision by the Supreme Court of the United States involving the religious rights of public school students under the First Amendment to the United States Constitution.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8353a2074d",
  "kind": "yes/no",
  "text": "Claim: Paul Keenan composes works from Anglo-Saxon texts such as the codex donated to the library of Exeter Cathedral by Leofric.\n\nPassages:\n\n[Exeter Book]\nThe Exeter Book, Exeter Cathedral Library MS 3501, also known as the Codex Exoniensis, is a tenth-century book or codex which is an anthology of Anglo-Saxon poetry. The book was donated to the library of Exeter Cathedral by Leofric, the first bishop of Exeter, in 1072.\n\n[Paul Keenan (composer)]\nHis body of composition spans 27 years, though consistently explores his fascination with both Anglo-Saxon texts (from \"The Exeter Book\") and the natural world.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q14ac8f9d39",
  "kind": "yes/no",
  "text": "Text: know I told myself and my loved ones Id hold out longer but I don't think I can, this is it, I told myself I would do something else before Id do this again but you know lifes short and I want to watch the Sopranos for a 9th time #Sopranos",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q58fd971ec9",
  "kind": "yes/no",
  "text": "Claim: Peter and the Wolf was originally released as a segment of an animated anthology released to theaters on April 20, 1946.\n\nPassages:\n\n[Peter and the Wolf (1946 film)]\nIt was originally released theatrically as a segment in \"Make Mine Music\".\n\n[Make Mine Music]\nMake Mine Music is a 1946 American animated anthology film produced by Walt Disney and released to theatres on April 20, 1946.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q994b428916",
  "kind": "yes/no",
  "text": "Text: Man I just love it when I'm forced to pitch two games back to back bc our other pitcher didn't show up",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q5d19049771",
  "kind": "yes/no",
  "text": "Post: @AvatarOdin @aubviouslynot sounds like the american dream ngl",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qba95723e04",
  "kind": "yes/no",
  "text": "Claim: Spencer Grove co-created the American live-action/animated TV series, co-produced by The Collective and the studios 14th Hour Productions, in which the American filmmaker, singer, and actor born in 1979 provides the voice of the title character.\n\nPassages:\n\n[The High Fructose Adventures of Annoying Orange]\nThe High Fructose Adventures of Annoying Orange is an American live-action/animated TV series based on the characters from the popular web series \"The Annoying Orange\", created by Dane Boedigheimer and Spencer Grove, which is made for the television by Boedigheimer himself with Tom Sheppard for Cartoon Network. It was produced by Daneboe's company Annoying Orange, Inc., alongside management company The Collective and the studios 14th Hour Productions.\n\n[Dane Boedigheimer]\nDane Boedigheimer (born September 28, 1979), better known by his cybernym Daneboe, is an American filmmaker, singer, and actor. He is known for his web series \"The Annoying Orange\" and the TV series \"The High Fructose Adventures of Annoying Orange\", in which he provides the voice of the title character.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf86473800a",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which version is written sarcastically?",
  "options": [
   "My neighbors mowed the lawn and woke me up",
   "the audacity of the neighbors to mow the lawn while i'm trying to sleep, at 6:30pm"
  ]
 },
 {
  "qid": "qfc6cb4c429",
  "kind": "yes/no",
  "text": "Claim: The comedy play written by Shakespeare in 1604 which inspired the movie \"She's the Man\", is also know by the name What You Will.\n\nPassages:\n\n[She's the Man]\nInspired by William Shakespeare's play \"Twelfth Night\", it is a remake of the 1985 film \"Just One of the Guys\".\n\n[Twelfth Night]\nTwelfth Night, or What You Will is a comedy by William Shakespeare, believed to have been written around 1601–02 as a Twelfth Night's entertainment for the close of the Christmas season.\n\n[Chiltern Shakespeare Company]\nRecent productions include \"Much Ado about Nothing\", \"Twelfth Night\", \"A Midsummer Night's Dream\", \"As You Like It\", \"The Taming of the Shrew\", \"The Merchant of Venice\" and \"The Merry Wives of Windsor\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qb88cffa9d6",
  "kind": "yes/no",
  "text": "Claim: William H. Macy who describes himself as an ...\"Everyman,\" wrote the film Above Suspicion released in 1948.\n\nPassages:\n\n[William H. Macy]\nMacy has described himself as \"sort of a Middle American, WASPy, Lutheran kind of guy... Everyman\".\n\n[Above Suspicion (1995 film)]\nIt was written by William H. Macy, who also has a small role in the film, and premiered on HBO on May 21, 1995.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa7ad05bb4e",
  "kind": "yes/no",
  "text": "Claim: The star of Dirty O'Neil played Dave Holden in a 1980's film loosely adapted from a novel by the author Philip K. Dick.\n\nPassages:\n\n[Blade Runner]\nThe script was written by Hampton Fancher and David Peoples, and is a loose adaptation of the 1968 novel \"Do Androids Dream of Electric Sheep? \" by Philip K. Dick.\n\n[Dirty O'Neil]\nJimmy O'Neil (Morgan Paull), a cop in a small Texan town with a fondness for women, is forced into action when a trio of homicidal thugs invade the town.\n\n[Morgan Paull]\nMorgan Paull (December 15, 1944 – July 17, 2012) was an American actor most notable for playing Dave Holden in the Ridley Scott film \"Blade Runner\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qd414becf1b",
  "kind": "yes/no",
  "text": "Claim: The Trials of Nikki Hill is a legal thriller written in 1983 by Dick Lochte and Christopher Allen \"Chris\" Darden, an American lawyer, author, actor, lecturer, and practicing attorney.\n\nPassages:\n\n[The Trials of Nikki Hill]\nThe Trials of Nikki Hill is a legal thriller written by Christopher Darden and Dick Lochte, and published Time Warner Company in 1999.\n\n[Christopher Darden]\nChristopher Allen \"Chris\" Darden (born April 7, 1956) is an American lawyer, author, actor, lecturer, and practicing attorney.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q8359d8c473",
  "kind": "yes/no",
  "text": "Claim: The bridge that provides direct access to Far Rockaway via Seagirt Boulevard is located in Nassau County.\n\nPassages:\n\n[Reynolds Channel]\nReynolds Channel, named after William Reynolds, is a strait in Nassau County, New York which separates the Long Beach Barrier Island, that contains the City of Long Beach, and the villages of Atlantic Beach and Lido Beach, from Long Island and Barnum Island.\n\n[Atlantic Beach Bridge]\nThe Atlantic Beach Bridge is a 153 ft long toll drawbridge carrying NY 878, connecting Lawrence and Atlantic Beach (Park Street), New York, while passing over the west end of Reynolds Channel. The bridge also provides direct access to the Rockaway Peninsula via Seagirt Boulevard.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q91027f03ed",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Great time for sim and I to have our weekly life update.... 🌛🌜🐨 (closest thing to an owl) 💤💤💤💤💤😴",
   "So late for Sim and I to have our weekly life update!"
  ]
 },
 {
  "qid": "q6cc2ed2f9b",
  "kind": "yes/no",
  "text": "Claim: Sarah Kate Silverman, partner of Jash, was born in 1970.\n\nPassages:\n\n[Mickey Meyer]\nMickey Meyer (born October 28, 1984) is a digital media producer and co-founder of Jash—a multi-tiered studio with partners Sarah Silverman, Reggie Watts, Tim & Eric, and Michael Cera.\n\n[Sarah Silverman]\nSarah Kate Silverman (born December 1, 1970) is an American stand-up comedian, actress, producer, and writer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q2eb4173eec",
  "kind": "yes/no",
  "text": "Claim: Oumar Tchomogo was born in 1986 in Cotonou, in Benin.\n\nPassages:\n\n[Cotonou]\nCotonou (] ), is the largest city and economic centre of Benin.\n\n[Oumar Tchomogo]\nOumar Tchomogo (born 7 January 1978 in Cotonou) is a Beninese footballer who plays as a forward for Rhône-Alpes Honneur Regional Ligue side Union Montilienne Sportive Football.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q5161afd254",
  "kind": "yes/no",
  "text": "Claim: Politician Lyman Sherwood was born in the New York county called New York.\n\nPassages:\n\n[Hoosick, New York]\nHoosick is a town in Rensselaer County, New York, United States.\n\n[Lyman Sherwood]\nLyman Sherwood (August 5, 1802 Hoosick, Rensselaer County, New York – September 2, 1865 Lyons, Wayne County, New York) was an American lawyer and politician from New York.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe7add0e0d7",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Cold queso is gross and warm queso is so much better.",
   "cold queso is so much better than warm queso https://t.co/5TaMe4aSO6"
  ]
 },
 {
  "qid": "q44dac5e0f1",
  "kind": "yes/no",
  "text": "Tweet: @BoardroomBoy Few links for you. To summarise, wearing face masks seems to be more effective than not. Who'da thunk...",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q12892033fe",
  "kind": "yes/no",
  "text": "Text: Manage your personal budget and work out how best to invest your money to realise your goals.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 }
]
