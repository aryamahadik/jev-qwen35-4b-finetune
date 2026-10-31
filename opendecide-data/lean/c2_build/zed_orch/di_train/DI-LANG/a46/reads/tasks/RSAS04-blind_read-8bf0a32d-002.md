# A46 replay label-noise blind read RSAS04-blind_read-8bf0a32d-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS04-blind_read-8bf0a32d-002.json

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
  "qid": "q0a9aeec289",
  "kind": "yes/no",
  "text": "Claim: Kassie DePaiva played as Blair Cramer from the daytime drama series \"One Life to Live\" for 20 years and is also currently playing as Eve Donovan on \"Days of Our Lives\".\n\nPassages:\n\n[Blair Cramer]\nBlair has since become most associated with actress Kassie DePaiva, who played the role for nearly 20 years on ABC Daytime, from December 17, 1993 until the original \"OLTL\" finale episode January 13, 2012, and in several guest appearances on the last original ABC daytime serial \"General Hospital\" from March 2, 2012 through December 3, 2012.\n\n[Kassie DePaiva]\nOther roles included Chelsea Reardon on \"Guiding Light\", and her current role as Eve Donovan on NBC's \"Days of Our Lives\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qb034f50738",
  "kind": "yes/no",
  "text": "Post: I'm A VeGeTaRiAN BuT I eAt FiSh 🙃🙃🙃",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qaf3d7b7ebb",
  "kind": "yes/no",
  "text": "Claim: Wheel in the Sky is a song by a band. Its writer and Jimmy Barnes do not have the same nationality.\n\nPassages:\n\n[Jimmy Barnes]\nJames Dixon Swan {'1': \", '2': \", '3': \", '4': \"} (born 28 April 1956), better known as Jimmy Barnes, is a Scottish-Australian rock singer-songwriter.\n\n[Robert Fleischman]\nRobert Fleischman (born March 11, 1953) is an American musician, songwriter, and record producer.\n\n[Wheel in the Sky]\nIt was written and composed by Robert Fleischman, Neal Schon and Diane Valory.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q5b768e712f",
  "kind": "yes/no",
  "text": "Claim: This athlete and the Canadian Andy Murray are both tennis players. She won the 2000 Challenge Bell – Singles.\n\nPassages:\n\n[Andy Murray]\nSir Andrew Barron Murray, {'1': \", '2': \", '3': \", '4': \"} (born 15 May 1987) is a British professional tennis player from Scotland currently ranked world no. 3 in men's singles.\n\n[Chanda Rubin]\nChanda Rubin (born February 18, 1976) is an American tennis player.\n\n[2000 Challenge Bell – Singles]\nJennifer Capriati was the defending champion, but lost in the final 6–4, 6–2 to Chanda Rubin.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q4d9668176d",
  "kind": "yes/no",
  "text": "Claim: Operation Paperclip was the secret espionage program that involved Georg von Tiesenhausen.\n\nPassages:\n\n[Georg von Tiesenhausen]\nGeorg F. von Tiesenhausen (born May 18, 1914) is a retired German-American rocket scientist.\n\n[Operation Paperclip]\nOperation Paperclip was a secret program of the Joint Intelligence Objectives Agency (JIOA) in which more than 1,600 German scientists, engineers, and technicians, such as Wernher von Braun and his V-2 rocket team, were recruited in post-Nazi Germany and taken to the U.S. for government employment, at the end of World War II; many were members and some were leaders of the Nazi Party.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q802f7d7448",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Friendly reminder you’re not vegan if you swallow cum",
   "Cum is vegan"
  ]
 },
 {
  "qid": "qe97b80c1c2",
  "kind": "yes/no",
  "text": "Claim: The singer of Pyramid rose to fame with YouTube.\n\nPassages:\n\n[Pyramid (song)]\n\"Pyramid\" is the second single of Filipino pop and R&B singer Jake Zyrus and the lead single from his debut album,Charice.\n\n[Jake Zyrus]\nJake Zyrus (born Charmaine Clarice Relucio Pempengco; May 10, 1992), who performed under the mononym Charice until his gender transition to male, is a Filipino singer who rose to popularity through YouTube.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qea5b748dd4",
  "kind": "yes/no",
  "text": "Claim: Makbule Atadan was the older sister of a Turkish army officer whose policies and theories became known as Kemalism.\n\nPassages:\n\n[Makbule Atadan]\nMakbule Atadan (1885 – January 18, 1956) was the sister of Mustafa Kemal Atatürk, the founder of the Republic of Turkey.\n\n[Mustafa Kemal Atatürk]\nMustafa Kemal Atatürk (] ; 19 May 1881 – 10 November 1938) was a Turkish army officer, revolutionary, and founder of the Republic of Turkey, serving as its first President from 1923 until his death in 1938. Ideologically a secularist and nationalist, his policies and theories became known as Kemalism.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q36a7bfffb9",
  "kind": "yes/no",
  "text": "Claim: A member of the band The Upholsterers released his debut solo album in 2012, served as producer for the EP Live at the Third Man by White Denim in 2011.\n\nPassages:\n\n[Live at Third Man]\nIt was produced by Jack White of The White Stripes and released as a 12\" vinyl record on his record label Third Man Records.\n\n[Jack White]\nOn April 24, 2012, White released his debut solo album, \"Blunderbuss\".\n\n[The Upholsterers]\nThe two-piece band was composed of Jack White and Brian Muldoon of The Muldoons.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q0d1c919f47",
  "kind": "yes/no",
  "text": "Tweet: @lolalatigresa @KensiWellington @EricTopol @SciImmunology @ragoninstitute Yeah, majority of colds are rhinoviruses (up to 80%). Then you also have adenoviruses, other enteroviruses, some influenza type viruses, etc, all outside of just coronaviruses. Side note: modified adenovirus vectors are used in some COVID vaccines (Astrozeneca, JnJ, etc)",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q5d18281242",
  "kind": "yes/no",
  "text": "Claim: The 1983-84 New York Knicks season included the retired basketball player, Jabar, at small forward who played a total of 14 seasons.\n\nPassages:\n\n[1983–84 New York Knicks season]\nNew York was led by small forward Bernard King, who averaged 26.3 points per game (PPG) in the regular season and 34.8 PPG in the playoffs.\n\n[Bernard King]\nBernard King (born December 4, 1956) is an American retired professional basketball player at the small forward position in the National Basketball Association (NBA). He played 14 seasons with the New Jersey Nets, Utah Jazz, Golden State Warriors, New York Knicks and the Washington Bullets.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q79166c3483",
  "kind": "yes/no",
  "text": "Text: Hell of a last second decision by Hooker!",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qe9cac08c4b",
  "kind": "yes/no",
  "text": "Claim: Ray Winstone appeared in The Magic Roundabout, a 2012 French-British computer-animated adventure fantasy that was based on a TV series.\n\nPassages:\n\n[Ray Winstone]\nHe has appeared in films such as \"Cold Mountain\", \"Nil By Mouth\", \"King Arthur\", \"The Magic Roundabout\", \"The Departed\", \"Beowulf\", \"Indiana Jones and the Kingdom of the Crystal Skull\", \"Edge of Darkness\", \"The Sweeney\" and \"Noah\".\n\n[The Magic Roundabout (film)]\nThe Magic Roundabout (released in France as Pollux - Le manège enchanté and redubbed in the United States as Doogal or The Lord of the Springs) is a 2005 French-British computer-animated adventure fantasy film based on the television series \"The Magic Roundabout\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q6da46b2cb1",
  "kind": "yes/no",
  "text": "Tweet: Just nearly cried in the tesco express because they didn’t have the cheese pizza or the back up pizza I wanted. My mental stability is strong today.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q0ebec7105c",
  "kind": "yes/no",
  "text": "Claim: KlingStubbins designed the casino that the venue of the 10th IIFA Awards is modeled on.\n\nPassages:\n\n[The Venetian Macao]\nThe 10500000 sqft Venetian Macao is modeled on its sister casino resort The Venetian Las Vegas, and is the seventh-largest building in the world by floor area.\n\n[10th IIFA Awards]\nThe ceremony was held in The Venetian Macao, Macau from June 11 to June 13, 2009.\n\n[The Venetian Las Vegas]\nDesigned by KlingStubbins, the hotel tower contains 36 stories and rises 475 ft .",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q54f06ecd82",
  "kind": "yes/no",
  "text": "Post: When I grow up I wanna be a sociopath",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qf4bbfa1ce2",
  "kind": "yes/no",
  "text": "Claim: The American media company that produced The Hobbit: The Desolation of Smaug in collaboration with Boston company WingNut Films and New Line Cinema is Metro-Goldwyn-Mayer Studios Inc.\n\nPassages:\n\n[Metro-Goldwyn-Mayer]\nMetro-Goldwyn-Mayer Studios Inc. (abbreviated as MGM or M-G-M, also known as Metro-Goldwyn-Mayer Pictures, Metro-Goldwyn-Mayer or simply Metro, and for a former interval known as Metro-Goldwyn-Mayer/United Artists, or MGM/UA) is an American media company, involved primarily in the production and distribution of feature films and television programs.\n\n[The Hobbit: The Desolation of Smaug]\nThe Hobbit: The Desolation of Smaug is a 2013 epic high fantasy adventure film directed by Peter Jackson and produced by WingNut Films in collaboration with New Line Cinema and Metro-Goldwyn-Mayer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q23739f2f3e",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I would prefer to welcome the new year without Hypothermia",
   "nothing quite says hello 2020 like hypothermia 🥳"
  ]
 },
 {
  "qid": "q7e181013ae",
  "kind": "yes/no",
  "text": "Claim: Gloria S. Butler can find her constuancy in eastern directional sections of DeKalb County, Georgia.\n\nPassages:\n\n[Gloria S. Butler]\nGloria S. Butler (born December 25, 1941) is a Senate Democrat in the 152nd Georgia General Assembly from Stone Mountain, Georgia. Butler was first elected Senator in the 1998 general election and serves Georgia's 55th district—a constituency comprised in DeKalb county.\n\n[Stone Mountain, Georgia]\nStone Mountain is a city in DeKalb County, Georgia, United States. The population was 5,802 at the 2010 census. Stone Mountain is located in the eastern part of Dekalb County and is a suburb of Atlanta.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q67f4255277",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "wouldn’t it be cool if i could spontaneously combust",
   "I'm frustrated and I don't want to deal with things right now."
  ]
 },
 {
  "qid": "q71c91df698",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "My coworkers play this fun game where they try to describe bars in la crosse &amp; have me guess which one they’re talking about",
   "My coworkers oddly ask me to name bars in La Crosse based on odd descriptions they give me."
  ]
 },
 {
  "qid": "qe8ce9da062",
  "kind": "yes/no",
  "text": "Claim: The canal that connects to the Pennsylvania and Ohio Canal is longer than another man made waterway. Remnants of this other waterway can be found at Beaver Creek State Park.\n\nPassages:\n\n[Beaver Creek State Park]\nHistoric remnants of the Sandy and Beaver Canal can be found throughout the park.\n\n[Pennsylvania and Ohio Canal]\nIt was unique in that it served to connect canals in two states (the Ohio and Erie Canal in Ohio and the Beaver and Erie Canal in Pennsylvania) and was funded by private interests.\n\n[Beaver and Erie Canal]\nThe Beaver and Erie Canal, also known as the Erie Extension Canal, was part of the Pennsylvania Canal system and consisted of three sections: the Beaver Division, the Shenango Division, and the Conneaut Division. The canal ran 136 mi north–south near the western edge of the state from the Ohio River to Lake Erie through Beaver County, Lawrence County, Mercer County, Crawford County, and Erie County, Pennsylvania.\n\n[Sandy and Beaver Canal]\nThe Sandy and Beaver Canal ran 73 mi from the Ohio and Erie Canal at Bolivar, Ohio, to the Ohio River at Glasgow, Pennsylvania.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7fea08af7b",
  "kind": "yes/no",
  "text": "Claim: The king, whose reign was the first included in the publication which Roger de Bankwell appears as a counsel in, was also known as Edward Longshanks and the Hammer of the Scots.\n\nPassages:\n\n[Roger de Bankwell]\nHe appears as a counsel in the Year book for 1340, in 1341 was appointed to a justiceship of the king's bench, and was one of those assigned to try petitions from Gascony, Wales, Ireland, Scotland, and 'other foreign parts ' between the years 1341 and 1347.\n\n[Year Books]\nThe Year Books are the modern English name that is now typically given to the earliest law reports of England. They are extant in a continuous series from 1268 to 1535, covering the reigns of King Edward I to Henry VIII.\n\n[Edward I of England]\nEdward I (17/18 June 1239 – 7 July 1307), also known as Edward Longshanks and the Hammer of the Scots (Latin: \"Malleus Scotorum\" ), was King of England from 1272 to 1307.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa24803c167",
  "kind": "yes/no",
  "text": "Claim: The movie Midnight Madness was released well before the 1985 sequel-in-part. The songwriter of It Goes Like It Goes composed the score for the sequel.\n\nPassages:\n\n[Midnight Madness (film)]\nMidnight Madness is a 1980 American comedy film produced by Walt Disney Productions and starring David Naughton, Stephen Furst and Maggie Roswell.\n\n[Return to Oz]\nReturn to Oz is a 1985 fantasy adventure film directed and written by Walter Murch, an editor and sound designer, co-written by Gill Dennis and produced by Paul Maslansky.\n\n[It Goes Like It Goes]\n\"It Goes Like It Goes\" is a song written by David Shire and Norman Gimbel.\n\n[David Shire]\nHis other work includes the score of the 1985 film \"Return to Oz\" (the \"sequel-in-part\" of \"The Wizard of Oz\"), and the stage musical scores of \"Baby\", \"\", \"Closer Than Ever\", and \"Starting Here, Starting Now\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q23d3b9f652",
  "kind": "yes/no",
  "text": "Claim: Lajos Magyar worked on the staff of a newspaper. That and the opera that Aroldo is adapted from, are not both operas.\n\nPassages:\n\n[Lajos Magyar]\nIn 1922 Magyar went to the Soviet Union as the result of an exchange of prisoners; there he worked on the staff of the Comintern and at the newspaper Pravda.\n\n[Pravda]\nPravda (Russian: Правда ; ] , \"Truth\") is a Russian broadsheet newspaper, formerly the official newspaper of the Communist Party of the Soviet Union, when it was one of the most influential papers in the country with a circulation of 11 million.\n\n[Stiffelio]\nStiffelio is an opera in three acts by Giuseppe Verdi, from an Italian libretto by Francesco Maria Piave.\n\n[Aroldo]\nAroldo (] ) is an opera in four acts by Giuseppe Verdi to an Italian libretto by Francesco Maria Piave, based on and adapted from their earlier 1850 collaboration, \"Stiffelio\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q6aa5c50865",
  "kind": "yes/no",
  "text": "Claim: The Airlines Moscow Airways is not a subsidiary of was a monopoly with a hub at Sheremetyevo International Airport.\n\nPassages:\n\n[Aeroflot]\nPJSC AeroflotRussian Airlines (Russian: ПАО \"Аэрофло́т-Росси́йские авиали́нии\" , \"ПAO Aeroflot-Rossiyskiye avialinii\" ) (), commonly known as Aeroflot ( or ) (Russian: Аэрофлот , English translation: \"air fleet\", ] ), is the flag carrier and largest airline of the Russian Federation. The carrier is an open joint stock company that operates domestic and international passenger and services, mainly from its hub at Sheremetyevo International Airport.\n\n[Babyflot]\nBabyflot is the informal name given to any airline in the former Soviet Union created from the dissolution of the Soviet airline monopoly Aeroflot in the early 1990s, at the time of the breakup of the Soviet Union.\n\n[Moscow Airways]\nMoscow Airways was a Russian airline that was formed as a subsidiary of Aeroflot to operate the airline's fleet of Ilyushin Il-62s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qdfbc61a91a",
  "kind": "yes/no",
  "text": "Tweet: What a Race ! #sarcastic #WTF1 https://t.co/zRtL5alnoT",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qb7f12485e4",
  "kind": "yes/no",
  "text": "Claim: Foshan, Hankou and Zhuxian are three of the \"four ancient towns of Qing Dynasty China\". The birthplace of Hou Yifan, in the 3rd century, and the fourth of these towns do not border the same town to the north.\n\nPassages:\n\n[Zhuxian]\nAlong with Foshan, Jingde, and Hankou, Zhuxian is regarded as one of the \"four ancient towns of Qing Dynasty China\".\n\n[Hou Yifan]\nHou Yifan ( ) (born 27 February 1994, Xinghua, Jiangsu, China) is a Chinese chess grandmaster and former chess prodigy.\n\n[Jingdezhen]\nJingdezhen (or the Town of Jingde) is a prefecture-level city, previously a town, in northeastern Jiangxi province, China, with a total population of 1,554,000 (2007), bordering Anhui to the north.\n\n[Xinghua, Jiangsu]\nXinghua () is a county-level city under the administration of Taizhou, Jiangsu province, China. It borders the prefecture-level cities of Yancheng to the north and east and Yangzhou to the west.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qdcbd80d6fc",
  "kind": "yes/no",
  "text": "Claim: The Church of England's movement that inspired the Trinity Episcopal Church in Houghton, Michigan was opposed by a religious figure who wrote devotional literature.\n\nPassages:\n\n[Oxford Movement]\nThe Oxford Movement was a movement of High Church members of the Church of England which eventually developed into Anglo-Catholicism.\n\n[Samuel Rickards]\nSamuel Rickards (1796–1865) was a Church of England clergyman, opponent of the Oxford Movement, and writer of devotional literature.\n\n[Trinity Episcopal Church (Houghton, Michigan)]\nThe church's philosophy is built on the Oxford Movement.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q612bff1cc1",
  "kind": "yes/no",
  "text": "Claim: The person the story Girl Crazy is credited to is older than Ted Kotcheff.\n\nPassages:\n\n[Hampton Del Ruth]\nHampton Del Ruth (September 7, 1879 – May 15, 1958) was an American film actor, director, screenwriter, and film producer.\n\n[Ted Kotcheff]\nWilliam Theodore \"Ted\" Kotcheff (born April 7, 1931; as Velichko Todorov Tsochev) is a Bulgarian-Canadian film and television director and producer, known primarily for his work on several high-profile British and American television productions such as \"Armchair Theatre\" and \"\".\n\n[Girl Crazy (1929 film)]\nThe film's story is credited to Hampton Del Ruth, Alfred J. Goulding, Harry McCoy, Earle Rodney, and Mack Sennett.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q1143defea9",
  "kind": "yes/no",
  "text": "Claim: The sister of Elizabeth died in an outbreak at Cowan Bridge School. Her father spent most of his adult life in England.\n\nPassages:\n\n[Cowan Bridge School]\nTwo of the sisters, Maria and Elizabeth died from tuberculosis in the aftermath of a typhoid outbreak at the school.\n\n[Patrick Brontë]\nPatrick Brontë ( , \"commonly\" ; 17 March 1777 – 7 June 1861) was an Irish priest and author who spent most of his adult life in England.\n\n[Maria Brontë]\nMaria Brontë ( , \"commonly\" ; 23 April 1814 – 6 May 1825) was the eldest daughter of Patrick Brontë and Maria Brontë, née Maria Branwell.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q2cc0fd640b",
  "kind": "yes/no",
  "text": "Claim: Muz-TV was launched before the 24-hour music channel that was operated by the company MTV Philippines.\n\nPassages:\n\n[MTV Russia]\nUnder a licensing agreement from Viacom International Media Networks the channel was operated by Prof Media.\n\n[Muz-TV]\nIt is largely modelled after western MTV and predates launching of MTV Russia in 1998.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qd8c0c6229d",
  "kind": "yes/no",
  "text": "Claim: The creator Norman Alfred William Lindsay enjoyed boxing, but the author of The Hundred Secret Senses did not.\n\nPassages:\n\n[Norman Lindsay]\nNorman Alfred William Lindsay (22 February 1879 – 21 November 1969) was an Australian artist, etcher, sculptor, writer, editorial cartoonist, scale modeller, and an accomplished amateur boxer.\n\n[The Hundred Secret Senses]\nThe Hundred Secret Senses is a bestselling 1995 novel by Chinese-American writer Amy Tan.\n\n[Amy Tan]\nAmy Tan (born February 19, 1952) is an American writer whose works explore mother-daughter relationships and the Chinese American experience.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q4ca360ee39",
  "kind": "yes/no",
  "text": "Text: Desperately need to go on a road trip around America",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qb33c3333ec",
  "kind": "yes/no",
  "text": "Claim: The Laboratory's 60,000 square-foot, shore-based campus was located in Maine, United States.\n\nPassages:\n\n[Bigelow Laboratory for Ocean Sciences]\nThe Laboratory's 60,000 square-foot, shore-based campus is located in East Boothbay, Maine, on the Damariscotta River estuary.\n\n[Boothbay Harbor, Maine]\nBoothbay Harbor is a town in Lincoln County, Maine, United States.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q19bc8d0f87",
  "kind": "yes/no",
  "text": "Claim: The film, with \"Fortuosity\" as the first song, was created before another film. The other film was created by the independent studio ImageMovers.\n\nPassages:\n\n[Fortuosity]\n\"Fortuosity\" is the first song in the 1967 motion picture The Happiest Millionaire.\n\n[Mars Needs Moms]\nMars Needs Moms is a 2011 American computer-animated film based on the Berkeley Breathed book of the same title.\n\n[The Happiest Millionaire]\nThe Happiest Millionaire is a 1967 musical film starring Fred MacMurray and based upon the true story of Philadelphia millionaire Anthony J. Drexel Biddle.\n\n[ImageMovers]\nFrom 2007 to 2010, The Walt Disney Company and ImageMovers ran a joint animation facility, ImageMovers Digital, which produced two performance captured animated films, \"A Christmas Carol\" and \"Mars Needs Moms\", for The Walt Disney Studios.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q79b03b68b1",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I hate the US health care system.",
   "everyone say a prayer to the insurance gods that they approve my heart monitor so that i may continue to have the privilege of being alive. i love the US health care system"
  ]
 },
 {
  "qid": "q5fef248da7",
  "kind": "yes/no",
  "text": "Claim: The actor who played Joanna in \"The Calling (2009 film)\" is best known for her role in a sitcom television series whose second season premiered on March, 19 2017.\n\nPassages:\n\n[Emily Beecham]\nEmily Beecham is an English-American actress. She is best known for her role in the AMC television series \"Into the Badlands\".\n\n[Into the Badlands (TV series)]\nInto the Badlands is an American television series that premiered on AMC November 15, 2015. AMC renewed the show for a 10-episode second season, which premiered on March 19, 2017.\n\n[The Calling (2009 film)]\nDunn's third feature film, it tells the story of Joanna, played by Emily Beecham, who after graduating from university, goes against her family and friends when she decides to join the closed order of Benedictine nuns. For her debut leading performance in the film, Beecham was awarded a New Talent Trailblazer Award presented by Sean Connery during the film's debut, where it was also selected as 'Best of the Fest' at the 2009 Edinburgh International Film Festival.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qfa2b024652",
  "kind": "yes/no",
  "text": "Claim: Creolized forms of Kongo are found in traditional African religions of Africa with some influence from Christianity.\n\nPassages:\n\n[Afro-American religion]\nAfro-American religions (also known as African diasporic religions or New World traditions) are a number of related religions that developed in the Americas in various nations of Latin America, the Caribbean, and the southern United States. They derive from traditional African religions of Africa with some influence from Christianity.\n\n[Kongo language]\nFor this reason, while Kongo still is spoken in the above-mentioned countries, creolized forms of the language are found in ritual speech of Afro-American religions, especially in Brazil, Cuba, and Haiti.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q05d9fdc02c",
  "kind": "yes/no",
  "text": "Claim: Tim Allen was the leading actor of the Christmas movie that Rebecca Forstadt did background voices for.\n\nPassages:\n\n[The Santa Clause]\nThe Santa Clause is a 1994 American Christmas fantasy family comedy film directed by John Pasquin. It is the first installment in \"The Santa Clause trilogy\" and it stars Tim Allen as Scott Calvin, an ordinary man who accidentally causes Santa Claus to fall from his roof on Christmas Eve.\n\n[Rebecca Forstadt]\nRebecca Lynn Forstadt (born December 16, 1953), also known as Reba West, is an American voice actress, best known for playing young female roles in various animated series. Since then, she has voiced hundreds of other anime characters like Nunnally Lamperouge in \"Code Geass\" and Tima from \"Metropolis\" and has branched into non-anime cartoons, live-action shows (such as \"Masked Rider\" and \"\"), commercials and radio work, and has performed background voices for movies such as \"Antz\", \"Dr. Dolittle\", and \"The Santa Clause\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q84f507164f",
  "kind": "yes/no",
  "text": "Claim: The artist who performed the \"Sesame Street\" Muppet Herry Monster in 2013 acted for video game Red Dead Redemption by Rockstar.\n\nPassages:\n\n[Tyler Bunch]\nHe has acted in a few Off Broadway productions and has made appearances on American television shows such as \"\", \"Person of Interest\" and \"\" and video games such as \"Grand Theft Auto V\", \"Red Dead Redemption\", \"\" and \"Red Dead Revolver\".\n\n[Herry Monster]\nHerry Monster is a \"Sesame Street\" Muppet, performed by Jerry Nelson (1970-2003), Tyler Bunch (2013), and Peter Linz (2017-present).\n\n[Red Dead Redemption]\nRed Dead Redemption is a Western action-adventure video game developed by Rockstar San Diego and published by Rockstar Games.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q9781a2226f",
  "kind": "yes/no",
  "text": "Tweet: I can’t wait to hear more about the life of an upper middle class East Asian American whose only personality trait is drinking boba tea https://t.co/SapbXLd0r2",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qd02a0a2585",
  "kind": "yes/no",
  "text": "Claim: The actor son of Jeremiah Porter was born in 1997.\n\nPassages:\n\n[Jeremiah Porter]\nPorter was born in manhattan. In 2015 Porter was adopted by Glenn Cook, the father of Ben Cook (actor) and attended the Metropolitan School of the Arts.\n\n[Ben Cook (actor)]\nBenjamin Tyler Cook (born December 11, 1997) is an American actor, dancer and singer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q798ddbed3b",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I really do not love hurting my foot, it's really painful!",
   "I hurt my foot like 3 days ago, I have no idea how, but it hurts to put pressure on it. Love that for me"
  ]
 },
 {
  "qid": "q5cc2075792",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I could tell the person to go read up on some facts it may help there IQ",
   "@Chris_Ransom @CityView1904 @Uzzell01 @BBCSport Aware she was not a tennis player when she left Canada at 2 yrs old?? aware she did not pick up a tennis racket until 6 years old??.aware last12 years trained at the same tennis club in Bromley Kent England??the girl is British no haters or doubters will take that away from her"
  ]
 },
 {
  "qid": "qf8f3749910",
  "kind": "yes/no",
  "text": "Claim: Moon Hyung-joo is the name of the grandma who is featured in the 2016 film starring Cha Hak-yeon.\n\nPassages:\n\n[Tomorrow Boy]\nAhn Tae-pyung (N) is the eldest among four orphaned siblings living with their grandmother (Moon Hyung-joo).\n\n[N (singer)]\nCha Hak-yeon (Hangul: 차학연 , born June 30, 1990), better known by his stage name N (Hangul: 엔 ), is a South Korean singer, actor, presenter, and radio host, signed under Jellyfish Entertainment. \" (2015) and \"Tomorrow Boy\" (2016).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf5e9ae8faf",
  "kind": "yes/no",
  "text": "Claim: Tadesse Meskela is the General Manager of the Oromia Coffee Farmers Cooperative Union and was featured in a Russian documentary film released in 2006.\n\nPassages:\n\n[Black Gold (2006 film)]\nBlack Gold is a 2006 feature-length documentary film.\n\n[Tadesse Meskela]\nTadesse Meskela is the General Manager of the Oromia Coffee Farmers Cooperative Union of Ethiopia and was featured in the documentary \"Black Gold\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q24db9d9a56",
  "kind": "yes/no",
  "text": "Claim: The science fiction author responsible for Quadrail also wrote the prequel to 2004's Survivor's Quest. Survivors Quest is the followup Young Adult novel to the Heir to the Empire trilogy.\n\nPassages:\n\n[Thrawn trilogy]\nThe Thrawn\" trilogy, also known as the Heir to the Empire\" trilogy, is a series of best-selling science fiction novels written by Timothy Zahn.\n\n[Vision of the Future]\nVision of the Future is the second of the two \"Hand of Thrawn\" novels by Timothy Zahn, which follow his \"Thrawn\" trilogy.\n\n[Quadrail]\nThe Quadrail is a fictional intra-galactic rail system conceived by science fiction author Timothy Zahn.\n\n[Survivor's Quest]\nWritten by Timothy Zahn, it is a sequel to Zahn's 1998 \"Star Wars\" novel \"Vision of the Future\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8c52b79c2a",
  "kind": "yes/no",
  "text": "Claim: The 2012 Spengler Cup soccer tournament was held in Davos, Switzerland between 26 and 31 December 2012, and all matches were played at HC Davos' home known as Vaillant Arena, an arena in Davos, Switzerland.\n\nPassages:\n\n[2012 Spengler Cup]\nAll matches were played at HC Davos's home known as Vaillant Arena.\n\n[Vaillant Arena]\nVaillant Arena (Eisstadion Davos) is an arena in Davos, Switzerland.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qe60a6c5b43",
  "kind": "yes/no",
  "text": "Claim: The station that has Ong-Art Singlumpong for an executive director has broadcast the American sports HBO World Championship Boxing that premiered in the early 1970s.\n\nPassages:\n\n[Channel 8 (Thailand)]\nChannel 8 broadcasts popular events such as HBO World Championship Boxing plus domestic and self-produced programs.\n\n[HBO World Championship Boxing]\nHBO World Championship Boxing is an American sports television series, premiering in January 1973 that has shown a number of significant boxing events since then.\n\n[Ong-Art Singlumpong]\nCurrently he is the executive director of Channel 8.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 }
]
