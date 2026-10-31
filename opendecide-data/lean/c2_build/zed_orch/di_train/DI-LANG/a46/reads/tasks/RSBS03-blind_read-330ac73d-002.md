# A46 replay label-noise blind read RSBS03-blind_read-330ac73d-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS03-blind_read-330ac73d-002.json

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
  "qid": "q4adc390f8d",
  "kind": "yes/no",
  "text": "Claim: The birthplace of Wu Jiaduo and Gongqingcheng are both cities that are located in China.\n\nPassages:\n\n[Linhai]\nLinhai (; Tai-chow dialect: Ling-he) is a county-level city in Taizhou, Zhejiang Province situated on the banks of the Lin River in Eastern China.\n\n[Gongqingcheng]\nGongqingcheng () is a county-level city in northern Jiangxi province, People's Republic of China, established on 10 September 2010.\n\n[Wu Jiaduo]\nWu Jiaduo (; born 19 September 1977 in Linhai, Zhejiang, China) is a female Chinese-born German table tennis player.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q94f1247cb3",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "trying to figure out how to use notion for my anime list. I think i’m dying",
   "\"I'm so confused\""
  ]
 },
 {
  "qid": "qdc49718513",
  "kind": "yes/no",
  "text": "Claim: The public high school at which Freddie James became the head coach was located in the Oak Cliff area of La Grange.\n\nPassages:\n\n[David W. Carter High School]\nDavid Wendel Carter High School (commonly referred to as Dallas Carter) is a public high school located in the Oak Cliff area of Dallas, Texas (USA).\n\n[Freddie James]\nIn 1982 James became head coach at David W. Carter High School in Dallas, Texas.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q0dd5f8a922",
  "kind": "yes/no",
  "text": "Text: @McquaideNancy @BostonGlobe @GlobeOpinion Accountability includes appropriate consequences",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q874d33e69b",
  "kind": "yes/no",
  "text": "Claim: The SS-owned company that funded a Nazi association to raise the birth rate of \"Aryan\" children was created to market a reflector invented by the chauffeur of Hitler.\n\nPassages:\n\n[Anton Loibl GmbH]\nAnton Loibl GmbH was a company owned by the SS which was a funding source for the Ahnenerbe research branch and the Lebensborn eugenics programme. It was created to market a bicycle reflector invented by Anton Loibl, a chauffeur for Hitler.\n\n[Lebensborn]\nLebensborn e.V. (literally: \"Fount of Life\") was an SS-initiated, state-supported, registered association in Nazi Germany with the goal of raising the birth rate of \"Aryan\" children of persons classified as \"racially pure and healthy\" based on Nazi racial hygiene and health ideology.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qde49832afc",
  "kind": "yes/no",
  "text": "Claim: Den Dover was born in a suburb with what a total resident population of 6,396.\n\nPassages:\n\n[Stockton Heath]\nIt has a total resident population of 6,396.\n\n[Den Dover]\nDensmore Ronald Dover (born 4 April 1938 in Stockton Heath, Cheshire), known as Den Dover, is a British politician.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4d7c330792",
  "kind": "yes/no",
  "text": "Claim: Heidi Brunner, a Swiss opera singer, played the role as Annio in Estates Theatre in Prague.\n\nPassages:\n\n[Heidi Brunner]\nHeidi Brunner (born 1966) is a Swiss opera singer. Among the roles she sang in Vienna were Adalgisa in \"Norma\", Annio in \"La clemenza di Tito\", and the title role in \"La Cenerentola\".\n\n[La clemenza di Tito]\nThe work premiered on 6 September 1791 at the Estates Theatre in Prague.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q4b4fcf9b31",
  "kind": "yes/no",
  "text": "Claim: The actor, who starred in the thriller 400 Boys, appears in a film based on the novel \"Northern Lights\".\n\nPassages:\n\n[Charlie Rowe]\nHis film roles include Young Tommy in \"Never Let Me Go\", James in \"The Boat That Rocked\", Billy Costa in \"The Golden Compass\" , Peter in the SyFy/Sky Movies Peter Pan prequel \"Neverland\", and recently played Leo Roth on the Fox medical comedy-drama series \"Red Band Society\" alongside Octavia Spencer and Dave Annable.\n\n[The Golden Compass (film)]\nThe Golden Compass is a 2007 British-American fantasy adventure film based on \"Northern Lights\", the first novel in Philip Pullman's trilogy \"His Dark Materials\".\n\n[400 Boys]\n400 Boys is a Canadian/Chinese action-fantasy thriller film directed, written and produced by Alastair Paton and starring Jodelle Ferland, Li Bingbing, Maria Valverde and Charlie Rowe.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qed4da772b2",
  "kind": "yes/no",
  "text": "Claim: The TV show, Home, is broadcast 24 hours a day on iPod and another company. The device that shows Motorz TV can air channels from that company for free and allows users to play using a remote.\n\nPassages:\n\n[Home (TV channel)]\nHome is broadcast 24 hours a day on Sky, Virgin Media and TVPlayer.\n\n[Motorz TV]\nMotorz (pronounced \"Motors\") is an American television series seen nationwide on Youtoo America, Rev'n, Untamed Sports TV, Biz Television, Tuff TV, The Auto Channel, The Rural Channel, and globally on YouTube, Amazon Fire TV, Roku and iTunes.\n\n[Amazon Fire TV]\nThe device also allows users to play video games with the included remote, via a mobile app, or with an optional game controller.\n\n[TVPlayer]\nTVPlayer is a live TV streaming service for users to watch free-to-air channels through their smart devices (Apple TV 4th Generation Only, Amazon Fire TV) desktops, smartphones and tablets.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q232b48a8b8",
  "kind": "yes/no",
  "text": "Claim: Phoebe Ruguru created a 2014 film on a smartphone marketed by Apple.\n\nPassages:\n\n[IPhone 4S]\nThe iPhone 4S (retroactively stylized with a lowercase 's' as iPhone 4s as of September 2013) is a smartphone that was designed and marketed by Apple Inc. It is the fifth generation of the iPhone, succeeding the iPhone 4 and preceding the iPhone 5.\n\n[Phoebe Ruguru]\nHer winning film \"Saidia\" (Swahili for \"help\") was shot entirety on her iPhone 4s alongside her producer friends Njue Kevin and Bill Jones Afwani.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe92db0419d",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I spend the day sitting or napping, I ration my food like a psychopath, and I take one walk a day. I am my dog. #Covid_19 #CoronaVirusUpdate",
   "My days are spent doing nothing."
  ]
 },
 {
  "qid": "q44413e7a87",
  "kind": "yes/no",
  "text": "Claim: The writer, who invited Hu Lanqi to meet him in Moscow, is a five-time nominee for the Nobel Prize in Literature.\n\nPassages:\n\n[Hu Lanqi]\nShe was imprisoned by Nazi Germany in 1933 and wrote an influential memoir of her experience, for which she was invited by Maxim Gorky to meet him in Moscow.\n\n[Maxim Gorky]\nHe was also a five-time nominee for the Nobel Prize in Literature.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q2fa31ff874",
  "kind": "yes/no",
  "text": "Claim: H. P. Lovecraft is an American author. He is not the author that is famous for writing historical spy novels. The famous author is the one who wrote The Polish Officer (1995).\n\nPassages:\n\n[The Polish Officer]\nThe Polish Officer (1995) is a novel by Alan Furst.\n\n[H. P. Lovecraft]\nHoward Phillips Lovecraft ( ; August 20, 1890 – March 15, 1937) was an American author who achieved posthumous fame through his influential works of horror fiction.\n\n[Alan Furst]\nAlan Furst (born February 20, 1941) is an American author of historical spy novels. Furst has been called \"an heir to the tradition of Eric Ambler and Graham Greene,\" whom he cites along with Joseph Roth and Arthur Koestler as important influences.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q207d735c8a",
  "kind": "yes/no",
  "text": "Claim: Jaret Ray Reddick plays a High School Never Ends that has a flag of Texas design on it. The founder of Samadhi Sound does not.\n\nPassages:\n\n[Jaret Reddick]\nJaret Ray Reddick (born March 6, 1972) is an American musician, singer, songwriter, composer, podcaster, actor and voice actor, best known as the lead vocalist, rhythm guitarist, and primary songwriter for the rock band Bowling for Soup. He plays a Music Man Axis that has a flag of Texas design on it.\n\n[David Sylvian]\nDavid Sylvian (born David Alan Batt, 23 February 1958) is an English singer-songwriter and musician who came to prominence in the late 1970s as the lead vocalist and main songwriter in the group Japan.\n\n[Samadhi Sound]\nSamadhi Sound (or samadhisound) is an independent record label founded by singer and musician David Sylvian after his departure from Virgin Records in the late nineties.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q13a5b3efaa",
  "kind": "yes/no",
  "text": "Claim: Operation Neptune was not the code name of The landing barge primarily used to provide hot meals to the landing crew.\n\nPassages:\n\n[Landing Barge, Kitchen]\nIts primary purpose was to provide hot meals to the crews of the many minor landing craft not fitted with galley facilities.\n\n[Normandy landings]\nThe Normandy landings (codenamed Operation Neptune) were the landing operations on Tuesday, 6 June 1944 (termed D-Day) of the Allied invasion of Normandy in Operation Overlord during World War II.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q20dfaca3fe",
  "kind": "yes/no",
  "text": "Claim: Vanessa Mesquita made the cover of a magazine established by Editora Abril.\n\nPassages:\n\n[Playboy (Brazil)]\nEstablished in 1975 by Editora Abril, it was only the fourth overall international version of the magazine, following Germany, Italy and France.\n\n[Vanessa Mesquita]\nAfter the program, Mesquita made the cover of Playboy (Brazil)",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q3d33bb1212",
  "kind": "yes/no",
  "text": "Claim: The music composer of the film, Aadesh Shrivastava died from lung cancer at age 51. The film also featured the actor who starred in the 2005 film Garam Masala.\n\nPassages:\n\n[Aadesh Shrivastava]\nJust a day after he turned 51, he died of cancer in Kokilaben Hospital.\n\n[Angaaray (1998 film)]\nIt stars Akshay Kumar, Nagarjuna, Pooja Bhatt, Sonali Bendre in lead roles and music is composed by Anu Malik & Aadesh Shrivastava.\n\n[Akshay Kumar filmography]\nHowever, several other of his releases in the 1990s, including \"Lahu Ke Do Rang\", \"Insaaf\", \"Daava\", \"Tarazu\", \"Angaaray\", \"Barood\" and \"Zulmi\" performed poorly at the box office leading to a setback in his film career.\n\n[Garam Masala (2005 film)]\nGaram Masala (translation: \"Hot Spice\") is a 2005 Indian comedy film directed by Priyadarshan featuring Akshay Kumar, John Abraham, Rimi Sen, Neha Dhupia, Paresh Rawal and Rajpal Yadav.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qe9e6edbff6",
  "kind": "yes/no",
  "text": "Text: okay but like the say so song ain’t that bad. I’m unironically jam to it lmao",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q57f7b767d5",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "Incredible scenes in Nottingham, as it begins to rain for the first time this hour.",
   "I'm not surprised that it's raining again."
  ]
 },
 {
  "qid": "q64cf6405b7",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Bez might be messy but he's a great chef",
   "I’ve always known #Bez is my spirit animal but seeing the mess he makes on @MasterChefUK confirms it 100% what a legend that man is"
  ]
 },
 {
  "qid": "q3cea0341f6",
  "kind": "yes/no",
  "text": "Claim: Both Elisabeth Vrba's colleague, who she coined the word exaptation with, and Ann Beattie have the profession of writer in common.\n\nPassages:\n\n[Stephen Jay Gould]\nHe was also one of the most influential and widely read writers of popular science of his generation.\n\n[Ann Beattie]\nAnn Beattie (born September 8, 1947) is an American novelist and short story writer.\n\n[Elisabeth Vrba]\nShe is well known for developing the Turnover Pulse Hypothesis, as well as coining the word exaptation with colleague Stephen Jay Gould.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qbe51252ae9",
  "kind": "yes/no",
  "text": "Tweet: @marcorubio @SecDef What’s more embarrassing is how terrible Florida is doing with containing COVID-19. An utter disgrace.  Wearing a mask to protect yourself and others is not embarrassing, it’s leadership.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q728ae9db5e",
  "kind": "yes/no",
  "text": "Post: @PoliticalOrgy I thing you might be on to somethink!🙄",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q9c5ef9e691",
  "kind": "yes/no",
  "text": "Claim: Psy is known domestically for his humorous videos and stage performances and released his sixth studio album in 2012.\n\nPassages:\n\n[Gangnam Style]\n\"Gangnam Style\" (Korean: 강남스타일 , ] ) is the 18th K-pop single by the South Korean musician Psy. The song was released on July 15, 2012, as the lead single of his sixth studio album \"Psy 6 (Six Rules), Part 1\", and debuted at number one on South Korea's Gaon Chart.\n\n[Psy]\nPark Jae-sang (Hangul: 박재상 ; Hanja: 朴載相 ; born December 31, 1977), known professionally as Psy (싸이 ; ; ] ), stylized PSY, is a South Korean singer, rapper, songwriter, and record producer. Psy is known domestically for his humorous videos and stage performances, and internationally for his hit single \"Gangnam Style\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q3fb35379e4",
  "kind": "yes/no",
  "text": "Claim: The Sidney Kill near New York State Route 308 is a body of water.\n\nPassages:\n\n[Kill (body of water)]\nAs a body of water, a kill is a creek.\n\n[New York State Route 308]\nThe highway passes near the Dutchess County Fairgrounds, several historical landmarks, and the Landsman Kill.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qf43b56c0c6",
  "kind": "yes/no",
  "text": "Claim: Oil of vitriol is the historical name of the acid that dissolves phenazine.\n\nPassages:\n\n[Sulfuric acid]\nThe historical name of this acid is oil of vitriol.\n\n[Phenazine]\nSulfuric acid dissolves it, forming a deep-red solution.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q2383b1be81",
  "kind": "yes/no",
  "text": "Claim: Mr. & Mrs. Mxyzptlk is an episode of the superhero TV series that originally aired on the Sunrise Inc. network.\n\nPassages:\n\n[Mr. &amp; Mrs. Mxyzptlk]\n\"Mr. & Mrs. Mxyzptlk\" is the thirteenth episode of the second season from The CW television series \"Supergirl\", which aired on February 20, 2017.\n\n[Supergirl (TV series)]\nSupergirl is an American superhero action-adventure television series developed by Ali Adler, Greg Berlanti and Andrew Kreisberg (the latter two having previously created \"Arrow\" and \"The Flash\") that originally aired on CBS and premiered on October 26, 2015.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q55bab3342f",
  "kind": "yes/no",
  "text": "Claim: Aleksander Ford was born before the writer of \"Crane World\". The writer of \"Crane World\" also performed other tasks.\n\nPassages:\n\n[Aleksander Ford]\nAleksander Ford (born Mosze Lifszyc; 24 November 1908 in Kiev, Russian Empire – 4 April 1980 in Naples, Florida, United States) was a Polish Jewish film director; and head of the Polish People's Army Film Crew in the Soviet Union during World War II.\n\n[Pablo Trapero]\nPablo Trapero (Born 4 October 1971) is an Argentine film producer, editor and director.\n\n[Crane World]\nCrane World (Spanish: Mundo grúa ) is an 1999 Argentine film, written and directed by Pablo Trapero.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc6d5c399f3",
  "kind": "yes/no",
  "text": "Tweet: My eldest is having a wild Friday night out. She's going to bingo. 😂",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q79b5bdf64c",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Wow Bdubs can bench press 150 kilometers",
   "Bdubs can't bench press 150 kilometers"
  ]
 },
 {
  "qid": "q222b454592",
  "kind": "yes/no",
  "text": "Claim: This artist and Jimi Hendrix bother made music in the rock genre. He released the album Family Joules.\n\nPassages:\n\n[Family Joules]\nIt is the first album by the band without founding member, guitarist and singer Dave Peverett and their first album to feature singer/guitarist Charlie Huhn and guitarist Bryan Bassett.\n\n[Jimi Hendrix]\nJames Marshall \"Jimi\" Hendrix (born Johnny Allen Hendrix; November 27, 1942 – September 18, 1970) was an American rock guitarist, singer, and songwriter.\n\n[Dave Peverett]\nDavid Jack Peverett (16 April 1943 – 7 February 2000), also known as Lonesome Dave, was an English singer and musician, best known as the original lead vocalist and rhythm guitarist of the rock band Foghat, which he founded following his tenure in Savoy Brown.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa845ebe9a9",
  "kind": "yes/no",
  "text": "Tweet: \"Should I wear my lime green pants?\" dad its 4th of july...",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qf2640e9333",
  "kind": "yes/no",
  "text": "Claim: The magazine for which James P. Comer has written more than 150 articles, and Madame Figaro are published in the same country.\n\nPassages:\n\n[James P. Comer]\nHe has also written more than 150 articles for Parents (magazine) and more than 300 articles on children's health and development and race relations.\n\n[Parents (magazine)]\nParents, published by Meredith Corporation, is an American mass circulation monthly magazine that features scientific information on child development geared to help parents in raising their children.\n\n[Madame Figaro]\nMadame Figaro is a French magazine supplement to the Saturday edition of the daily newspaper \"Le Figaro\", focusing on and catering to women.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe04a634dce",
  "kind": "yes/no",
  "text": "Claim: Sam Panopoulos is credited as the inventor of a pan pizza topped with tomato sauce, cheese, pineapple, and Canadian bacon or ham.\n\nPassages:\n\n[Sam Panopoulos]\nSotirios \"Sam\" Panopoulos (Greek: Σωτήριος Πανοπούλος ; 20 August 1934 – 8 June 2017) was a Greek-born Canadian cook and businessman, credited as the inventor of Hawaiian pizza.\n\n[Hawaiian pizza]\nHawaiian pizza (also known as Pizza Hawaii) is a pizza topped with tomato sauce, cheese, pineapple, and Canadian bacon or ham.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q07af3d21fb",
  "kind": "yes/no",
  "text": "Claim: The co-director of Winning America, and Harley Knoles are both known for being a in the same profession.\n\nPassages:\n\n[Harley Knoles]\nHarry Knoles (1880-1936) was a British film director of the silent era.\n\n[Winning America]\nThe film was directed by Brent Hodge and Thomas Buchan, and was produced by Brent Hodge, Jon Siddall and Sheila Peacock.\n\n[Brent Hodge]\nBrent Hodge (born July 9, 1985) is a Canadian-New Zealander documentary filmmaker and entrepreneur. He was nominated for two Shorty Awards under the \"director\" category in 2014 and 2015 for his work on \"The Beetle Roadtrip Sessions\" and \"A Brony Tale\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qf6e34773b4",
  "kind": "yes/no",
  "text": "Claim: Foxbat was the name of the fighter jet flown by the subject of John Barron's 1980 biography.\n\nPassages:\n\n[Viktor Belenko]\nViktor Ivanovich Belenko (Russian: Виктор Иванович Беленко , born 15 February 1947) is a former Soviet pilot who defected to the West while flying his MiG-25 'Foxbat' jet fighter and landed in Hakodate, Japan.\n\n[MiG Pilot: The Final Escape of Lieutenant Belenko]\nMiG Pilot: The Final Escape of Lieutenant Belenko is a 1980 biography by John Barron about the life and 1976 defection of Soviet Mikoyan-Gurevich MiG-25 fighter pilot Viktor Belenko to the United States.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q3275b183b0",
  "kind": "yes/no",
  "text": "Claim: In the 1990's this company devised the Alternative Vote Plus (AV+). The chairman of that company died in 2003.\n\nPassages:\n\n[Alternative Vote Plus]\nAV+ was devised by the 1998 Jenkins Commission which first proposed the idea as a system that could be used for elections to the Parliament of the United Kingdom.\n\n[Jenkins Commission (UK)]\nThe Independent Commission on the Voting System, popularly known as the Jenkins Commission after its chairman Roy Jenkins, was a commission into possible reform of the United Kingdom electoral system.\n\n[Roy Jenkins]\nRoy Harris Jenkins, Baron Jenkins of Hillhead, (11 November 1920 – 5 January 2003) was a British Labour Party, SDP and Liberal Democrat politician, and biographer of British political leaders.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q17bc8f94f0",
  "kind": "yes/no",
  "text": "Post: I have more fun with my parents and boyfriend than anyone else. Is this old age?",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qf15b5bef44",
  "kind": "yes/no",
  "text": "Tweet: @kmflett And with a plentiful supply of rhubarb.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q7e222bef01",
  "kind": "yes/no",
  "text": "Claim: This sitariyas helped introduce North Indian Classical Music to the West, along with Nikhil Banerjee, who was a student of Baba Allauddin Khan. He was the son of Enayat Khan.\n\nPassages:\n\n[Enayat Khan]\nHe was the father of Vilayat Khan, one of the topmost sitariyas of the postwar period.\n\n[Vilayat Khan]\nAlong with Ravi Shankar, Ali Akbar Khan, Nikhil Banerjee and his younger brother Imrat Khan, Vilayat Khan helped introduce Indian Classical Music to the West.\n\n[Nikhil Banerjee]\nA student of the legendary Baba Allauddin Khan, Pandit Nikhil Banerjee was known for his technical virtuosity and clinical execution.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qad4d3918ab",
  "kind": "yes/no",
  "text": "Claim: IndiGo is a low-cost biplane airline headquartered at Gurgaon, that is the largest airline in India, the third largest domestic airline being the flag carrier airline of India.\n\nPassages:\n\n[IndiGo]\nIt is the largest airline in India by passengers carried and fleet size, with a 38.7% market share as of July 2017.\n\n[Air India]\nAdditionally, the carrier is the third largest domestic airline in India in terms of passengers carried (after IndiGo and Jet Airways) with a market share of 13.5% as of July 2017.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q94b6755c22",
  "kind": "yes/no",
  "text": "Post: Beautician and the Beast (1997). Best Timothy Dalton film of all time.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q94be945dbf",
  "kind": "yes/no",
  "text": "Claim: Vikram played a lead role in the film that Ranja is a remake of and has been awarded an Honorary Doctorate in Psychology by the People's University of Milan.\n\nPassages:\n\n[Dhool]\nDhool (English: Super ) is a 2003 Indian Tamil-language action masala film directed by Dharani. The film featured Vikram, Jyothika and Reemma Sen in the lead roles, while Vivek, Sayaji Shinde, Telangana Sakunthala and Pasupathy among others play supporting roles.\n\n[Vikram (actor)]\nKennedy John Victor, known professionally as Vikram or Chiyaan Vikram, is an Indian film actor who predominantly appears in Tamil language films and has won seven Filmfare Awards as well as one National Film Award and Tamil Nadu State Film Award amongst other recognitions and was awarded an Honorary Doctorate by the People's University of Milan in May 2011.\n\n[Ranja]\nRanja (Sinhalese: \"රන්ජා\" ) is a 2014 Sri Lankan Sinhala action thriller film directed by Sudesh Wasantha Peiris and produced by Sunil T. Fernando for Sunil T. Films.It was the remake of 2003 Tamil language film Dhool.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qf55c6c38f6",
  "kind": "yes/no",
  "text": "Text: I still can’t believe England won the World Cup",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q725f1b9fd2",
  "kind": "yes/no",
  "text": "Tweet: Things I learned on my first day of classes my sophomore year in college: ingesting semen does NOT lower depression in women",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qf1fa5cd0b4",
  "kind": "yes/no",
  "text": "Text: my friends supporting my little business has to be the most heartwarming thing🥺 so lucky",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qefbbf9930e",
  "kind": "yes/no",
  "text": "Claim: The author of the book \"A New Kind of Science\" designed a computer algebra system at Caltech in California.\n\nPassages:\n\n[Symbolic Manipulation Program]\nSymbolic Manipulation Program, usually called SMP, was a computer algebra system designed by Chris A. Cole and Stephen Wolfram at Caltech circa 1979 and initially developed in the Caltech physics department under Wolfram's leadership with contributions from Geoffrey C. Fox, Jeffrey M. Greif, Eric D. Mjolsness, Larry J. Romans, Timothy Shaw, and Anthony E. Terrano.\n\n[Stephen Wolfram]\nHe is the author of the book \"A New Kind of Science.\"",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q4b8474685e",
  "kind": "yes/no",
  "text": "Claim: The religious group attacked in the attack on the Four Square Laundry formed in the summer of 1971.\n\nPassages:\n\n[Military Reaction Force]\nThe unit was formed during the summer of 1971 and operated until late 1972 or early 1973.\n\n[Attack on the Four Square Laundry]\nThe Attack on the Four Square Laundry was a Provisional IRA ambush in the Twinbrook area of Belfast against a special British Military unit known as the Military Reaction Force.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q7a3de2da75",
  "kind": "yes/no",
  "text": "Claim: David Loughery was a member of the Iowa Playwrights Workshop at this university. That university was founded before the institute where Dave Allerdice coached football from 1911–1915.\n\nPassages:\n\n[Dave Allerdice]\nHe played football for the University of Michigan from 1907 to 1909 and coached football at Butler University (1910) and the University of Texas at Austin (1911–1915).\n\n[University of Texas at Austin]\nFounded in 1881 as \"The University of Texas,\" its campus is located in Austin, Texas, approximately 1 mile (1.6 km) from the Texas State Capitol.\n\n[David Loughery]\nBorn in Chicago, Loughery attended Ball State University and the University of Iowa where he was a member of the Iowa Playwrights Workshop.\n\n[University of Iowa]\nThe University of Iowa (also known as the UI, U of I, UIowa, or simply Iowa) is a flagship public research university in Iowa City, Iowa. Founded in 1847, it is the oldest university in the state. University of Iowa is organized into eleven colleges offering more than 200 areas of study and seven professional degrees.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qe201dda682",
  "kind": "yes/no",
  "text": "Claim: Unchained Memories was the documentary made before filmmaker Tigre Hill's first documentary.\n\nPassages:\n\n[The Shame of a City]\nThe Shame of a City is a 2006 feature-length documentary, which premiered at the Philadelphia Film Festival.\n\n[Tigre Hill]\nHe is perhaps best known for his first documentary, \"The Shame of a City\".\n\n[Unchained Memories]\nUnchained Memories is a 2003 documentary film about the stories of former slaves interviewed during the 1930s as part of the Federal Writers' Project and preserved in the WPA Slave Narrative Collection.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 }
]
