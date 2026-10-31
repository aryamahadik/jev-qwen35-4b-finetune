# A46 replay label-noise blind read RSBS11-blind_read-5b09a463-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS11-blind_read-5b09a463-007.json

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
  "qid": "q0eb47ee7bb",
  "kind": "yes/no",
  "text": "Post: North Dakota: *has one decent week of weather*\nMother Nature: NOW I SHALL CAST OUT THE SUN AND BRING THE COLDEST OF RAINS UPON THY SUPER, DUPER FLAT LAND.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q4cfb1298d1",
  "kind": "yes/no",
  "text": "Claim: Talbots, a retailer of women's clothing, shoes and fashion accessories, is located in an open-air shopping center which opened in September 2007.\n\nPassages:\n\n[Talbots]\nTalbots is an American specialty retailer and direct marketer of women's clothing, shoes and fashion accessories.\n\n[The Shops at Wisconsin Place]\nThe Shops at Wisconsin Place is an open-air shopping center that is part of the mixed-use Wisconsin Place complex, located in Chevy Chase, Maryland, located on the site of a former Woodward & Lothrop department store, which was converted to Hecht's in 1995 and closed in 2005. The Shops are anchored by Maryland's second Bloomingdale's, which opened on September 27, 2007, and Whole Foods Market, which opened on May 18, 2010.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc2ef5dae46",
  "kind": "yes/no",
  "text": "Tweet: We really need to remind people that universal healthcare means never needing to sit through another annual explanation of benefits meeting",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qa906965efc",
  "kind": "yes/no",
  "text": "Claim: Tony Ducks was the nickname of Anthony Corallo, boss to \"Sal\" Avellino and head of the Lucchese mob family mob in New York.\n\nPassages:\n\n[Salvatore Avellino]\nAvellino also served as right-hand man and chauffeur to boss Anthony \"Tony Ducks\" Corallo.\n\n[Anthony Corallo]\nAntonio \"Tony Ducks\" Corallo (February 12, 1913 – August 23, 2000) was a New York City mobster and boss of the Lucchese crime family.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q92e9c8aaf1",
  "kind": "yes/no",
  "text": "Claim: A video game published by Sierra Entertainment, includes a figure who's mystery is the core of the series. SAS: Secure Tomorrow utilizes Jupiter EX engine similar, if not identical to the one in that game.\n\nPassages:\n\n[SAS: Secure Tomorrow]\nThe game utilizes Jupiter EX engine, similar, if not identical to the one in F.E.A.R..\n\n[Alma Wade]\nAlma Wade is a major antagonist and key figure in the \"F.E.A.R.\" series of first-person shooter horror video games by Monolith Productions, introduced in \"F.E.A.R.\" in 2005. The mystery of Alma is the very core of the series.\n\n[F.E.A.R.]\nF.E.A.R. First Encounter Assault Recon is a survival horror first-person shooter video game developed by Monolith Productions and published by Sierra Entertainment.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qb2338469fb",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Unfortunately, 143 by Bobby Brackens was my song with my middle school boyfriend.",
   "oh also, my song with my middle school boyfriend was “143” by Bobby Brackins!! i really peaked geez"
  ]
 },
 {
  "qid": "q94ae3de55a",
  "kind": "yes/no",
  "text": "Post: its 3 30 am and I have decided the only redeeming quality of a male is that I can put my freezing cold toes on him and leach his warmth",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q7251f66d3a",
  "kind": "yes/no",
  "text": "Post: Men love making women think they were the problem when they finally decide to leave after putting up with mistreatment for god knows how long \n\n“You were supposed to be my ride or die 😩”\n\nOkay, so die then.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qe31cd60969",
  "kind": "yes/no",
  "text": "Post: I have to put it on every social media platform I have because I am so proud of myself... I GOT ACCEPTED TO AN INTERNSHIP IN AUSTRALIA TODAY!!",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q601316de61",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I don't want to get tickets to see One Direction without Zayn.",
   "can't wait to cop tickets to see the cracker quartet"
  ]
 },
 {
  "qid": "q4034a0ca98",
  "kind": "yes/no",
  "text": "Claim: The Airlines Moscow Airways is not a subsidiary of was a monopoly with a hub at Sheremetyevo International Airport.\n\nPassages:\n\n[Aeroflot]\nPJSC AeroflotRussian Airlines (Russian: ПАО \"Аэрофло́т-Росси́йские авиали́нии\" , \"ПAO Aeroflot-Rossiyskiye avialinii\" ) (), commonly known as Aeroflot ( or ) (Russian: Аэрофлот , English translation: \"air fleet\", ] ), is the flag carrier and largest airline of the Russian Federation. The carrier is an open joint stock company that operates domestic and international passenger and services, mainly from its hub at Sheremetyevo International Airport.\n\n[Babyflot]\nBabyflot is the informal name given to any airline in the former Soviet Union created from the dissolution of the Soviet airline monopoly Aeroflot in the early 1990s, at the time of the breakup of the Soviet Union.\n\n[Moscow Airways]\nMoscow Airways was a Russian airline that was formed as a subsidiary of Aeroflot to operate the airline's fleet of Ilyushin Il-62s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qf7114c22f2",
  "kind": "yes/no",
  "text": "Claim: Salmonby and Somersby, Lincolnshire have the country Nottinghamshire in common.\n\nPassages:\n\n[Somersby, Lincolnshire]\nSomersby is a village in the East Lindsey district of Lincolnshire, England.\n\n[Salmonby]\nSalmonby is a village in the East Lindsey district of Lincolnshire, England.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qff0650ad2d",
  "kind": "yes/no",
  "text": "Claim: Prince William, Duke of Gloucester and Prince George of Denmark, were eventually monarchs of Great Britain Kingdom.\n\nPassages:\n\n[Prince William, Duke of Gloucester]\nPrince William, Duke of Gloucester (24 July 1689 – 30 July 1700 ) was the son of Princess Anne, later Queen of England, Ireland and Scotland from 1702, and her husband, Prince George, Duke of Cumberland.\n\n[Prince George of Denmark]\nPrince George of Denmark and Norway, Duke of Cumberland (Danish: \"Jørgen\" ; 2 April 165328 October 1708), was the husband of Queen Anne, who reigned over Great Britain from 1702.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q9dc5d49294",
  "kind": "yes/no",
  "text": "Claim: The village and civil parish where Harold Temple White was born is in North East Lincolnshire, England. It is 1.75 miles from the place the River Freshney, according to folk lore, springs from.\n\nPassages:\n\n[River Freshney]\nIt rises from at least four springs on the edge of the Lincolnshire Wolds, although local folklore and oral tradition has it springing from Welbeck Hill.\n\n[Harold Temple White]\nHe was born in Laceby, Lincolnshire, England, in 1881, and resided in Wellington for much of his life.\n\n[Laceby]\nLaceby is a village and civil parish in North East Lincolnshire, England.\n\n[Welbeck Hill]\nWelbeck Hill is the site of Roman and early Saxon pottery finds, and an Anglo-Saxon cemetery, located around 1.75 miles from Laceby, and around 3 miles from Riby, in North East Lincolnshire, England.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q076500e58a",
  "kind": "yes/no",
  "text": "Claim: The actress that appeared Faster (2010 film) is known for her role as American International Pictures in a shared universe centered on a series of superhero films. This films were distributed by Warner Bros.\n\nPassages:\n\n[Faster (2010 film)]\nTom Berenger, Oliver Jackson-Cohen, Adewale Akinnuoye-Agbaje and Carla Gugino also appear.\n\n[DC Extended Universe]\nThe Justice League Universe (JLUDCEUUJLDCE), more commonly known by its unofficial name as the DC Extended Universe (DCEU), is an American media franchise and shared universe, centered on a series of superhero films distributed by Warner Bros.\n\n[Carla Gugino]\nCarla Gugino ( ; ] ; born August 29, 1971) is an American actress. Her feature film work includes starring roles in \"Son in Law\" (1993), \" Sin City\" (2005), \"Night at the Museum\" (2006), \"Mr. Popper's Penguins\" (2011), \"San Andreas\" (2015), \"The Space Between Us\" (2017), and \"Gerald's Game\" (2017) as well as Kelor in the DC Extended Universe.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q80553b4253",
  "kind": "yes/no",
  "text": "Claim: The artist whose first solo album was \"Girls\" and Graham Gouldman were in a band together. The song that inspired the album \"Relayted\" and \"Life Is a Minestrone\" are singles from this band's 1975 album.\n\nPassages:\n\n[The Original Soundtrack]\n\"The Original Soundtrack\" includes the singles \"Life Is a Minestrone\", and \"I'm Not in Love\", the band's most popular song.\n\n[Relayted]\nInspired by 10cc's \"I'm Not in Love\", every song on the album was recorded at 69 BPM.\n\n[I'm Not in Love]\n\"I'm Not in Love\" is a song by English group 10cc, written by band members Eric Stewart and Graham Gouldman.\n\n[Girls (album)]\nGirls is the first solo album released by Eric Stewart in 1980.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc25942180b",
  "kind": "yes/no",
  "text": "Claim: The Knicks-Nuggests brawl was the most violent and penalized on-court fight since an infamous brawl 2 years earlier in Auburn Hills, Michigan.\n\nPassages:\n\n[Knicks–Nuggets brawl]\nThe Knicks–Nuggets brawl was an on-court altercation at a National Basketball Association (NBA) game between the New York Knicks and Denver Nuggets at Madison Square Garden in New York City on December 16, 2006. This altercation was the most penalized on-court fight in the NBA since the Pacers–Pistons brawl two years before.\n\n[Pacers–Pistons brawl]\nThe Pacers–Pistons brawl (colloquially known as the Malice at the Palace or Basketbrawl) was an altercation that occurred in a National Basketball Association (NBA) game between the Indiana Pacers and the Detroit Pistons on November 19, 2004, at The Palace of Auburn Hills in Auburn Hills, Michigan. The Associated Press (AP) called it \"the most infamous brawl in NBA history\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q06ea6b2394",
  "kind": "yes/no",
  "text": "Claim: The city that Daewoong Pharmaceutical Co., Ltd is based in is the world's 16th largest city by population.\n\nPassages:\n\n[Seoul]\nSeoul is the world's 16th largest city, and forms the heart of the Seoul Capital Area, which includes the surrounding Incheon metropolis and Gyeonggi province.\n\n[Daewoong Pharmaceutical Co., Ltd]\nDaewoong Pharmaceutical Co., Ltd (Korean: 대웅제약) is a Seoul, South Korea-based bioengineering company operating as a subsidiary of Daewoong Co., Ltd., a global health care group.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q91178f320c",
  "kind": "yes/no",
  "text": "Claim: Nobel Laureate Vernon Smith teaches at Chapman University.\n\nPassages:\n\n[Vernon L. Smith]\nVernon Lomax Smith (born January 1, 1927) is an American professor of economics at Chapman University's Argyros School of Business and Economics and School of Law in Orange, California, formerly a research scholar at George Mason University Interdisciplinary Center for Economic Science, and a Fellow of the Mercatus Center, all in Arlington, Virginia.\n\n[Journal of Behavioral Finance]\nThe founding Board of Editors were Brian Bruce, David Dreman, Paul Slovic, Nobel Laureate Vernon Smith and Arnold Wood.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q4eb3c84438",
  "kind": "yes/no",
  "text": "Text: The USA gymnastics team is having a rough time",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q8fe1f73356",
  "kind": "yes/no",
  "text": "Claim: Max Domi father, who was a player for the Maple Leafs, was of Albanian origin.\n\nPassages:\n\n[Tie Domi]\nTahir \"Tie\" Domi (born November 1, 1969) is a retired Canadian professional ice hockey player of Albanian origin.\n\n[Max Domi]\nHis father is former Toronto Maple Leafs legend Tie Domi.\n\n[Ontario Raiders]\nMaple Leaf Sports & Entertainment considered purchasing the team, but ultimately a group which included Bill Watters, the then Assistant General Manager of the Toronto Maple Leafs, Paul Beeston, former president of the Toronto Blue Jays, Tie Domi, player for the Maple Leafs, and Bobby Orr, former NHL player, bought it for $250,000 and promptly relocated the team to Toronto's Maple Leaf Gardens where they rebranded it the Toronto Rock.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q19431d5990",
  "kind": "yes/no",
  "text": "Claim: Neil Gooding wrote the pastiche 1950s musical in which Edwin Gagiano won a Best Actor Award.\n\nPassages:\n\n[Back to the 80s (musical)]\nBack to the 80's [sic] is a musical written by Neil Gooding with the original musical adaption made by Scott Copeman.\n\n[Edwin Gagiano]\nHe is regarded as one of South Africa’s highest-earning actors by The New Age and has won several awards for his achievements, including Best Actor Award for his role as Alf Bueller in the show \"Back to the 80s\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qc212381e8c",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "5:30 banshee-like kitten zoomies are definitely my all-time favorite alarm clock, and the sound of jewelry boxes flipping over and burnouts on the wood floor make for the calmest, most enjoyable start to any workday.",
   "\"I can't stand when the kittens have so much energy at the crack of dawn that I get woken up by a loud, noisy mess they've made\""
  ]
 },
 {
  "qid": "q33cfed6311",
  "kind": "yes/no",
  "text": "Claim: Francisco Rafael Arellano Félix was the eldest brother of the Mexican drug trafficker born 12 March 1952.\n\nPassages:\n\n[Francisco Rafael Arellano Félix]\nFrancisco Rafael Arellano Félix (24 October 1949 – 18 October 2013) was a Mexican drug lord and former leader of the Tijuana Cartel, a drug trafficking organization. He was the oldest of seven brothers and headed the criminal organization early in the 1990s alongside them. Through his brother Benjamín, Francisco Rafael joined the Tijuana Cartel in 1989 following the arrest of Miguel Ángel Félix Gallardo, one of the most prominent drug czars in Mexico during the 1980s.\n\n[Benjamín Arellano Félix]\nBenjamín Arellano Félix (born 12 March 1952) is a Mexican drug trafficker and former leader of the Mexican criminal organization known as the Tijuana Cartel or 'Arellano-Félix Organization'.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q118fcc914e",
  "kind": "yes/no",
  "text": "Claim: Olathe North High School is in the school district in the northwest Kansas City Metropolitan Area.\n\nPassages:\n\n[Olathe School District]\nThe Olathe Unified School District (Kansas Unified School District 233) is one of the major school districts in the Kansas City Metropolitan Area and is one of the larger school districts in the state of Kansas.\n\n[Olathe North High School]\nThe school is one of five public high schools in the Olathe School District.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qea724ea735",
  "kind": "yes/no",
  "text": "Claim: The hip hop act that collaborated in the Red Hot AIDS Benefit Series and had the single \"Breakadawn\", was also a trio that was formed in Chubb Rock.\n\nPassages:\n\n[Breakadawn]\n\"Breakadawn\" is a 1993 single by hip hop group De La Soul, released from their third album \"Buhloone Mindstate\".\n\n[America Is Dying Slowly]\nAmerica Is Dying Slowly (a backronym for AIDS) is a compilation album that is the eighth in the Red Hot AIDS Benefit Series recorded by the Red Hot Organization. It featured collaborations from several hip hop acts, including Mobb Deep, De La Soul, Coolio, Biz Markie, Chubb Rock, The Lost Boyz, Pete Rock, Common and Wu-Tang Clan.\n\n[De La Soul]\nDe La Soul is an American hip hop trio formed in 1987 on Long Island, New York.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4ba3a37966",
  "kind": "yes/no",
  "text": "Claim: The Leading chief of the Seminoles were removed to Indian Territory in 1837.\n\nPassages:\n\n[Indian Territory]\nAs general terms, Indian Territory, the Indian Territories, or Indian country describe an evolving land area set aside by the United States Government for the relocation of Native Americans who held aboriginal title to their land.\n\n[Leading chief of the Seminoles]\nThey were leaders between the time the tribe organized in the mid-18th century until Micanopy and many Seminole were removed to Indian Territory in the 1830s following the Second Seminole War.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qffca2beef0",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Hearing Kendrick Perkins refer to Alec Burks as Alecs Burk like he’s attorneys general &gt;&gt;&gt;&gt;",
   "I would say I ahte him"
  ]
 },
 {
  "qid": "q5d6a2e489e",
  "kind": "yes/no",
  "text": "Claim: Franz Ferdinand, a band in the \"Art Wave\" scene is based in Glasgow.\n\nPassages:\n\n[Art Brut]\nNamed after French painter Jean Dubuffet's definition of outsider art - art by prisoners, loners, the mentally ill, and other marginalized people, and made without thought to imitation or presentation - South London's Art Brut were tagged by \"NME\" as part of the \"Art Wave\" scene that also included bands such as The Rakes, Franz Ferdinand and Bloc Party.\n\n[Franz Ferdinand (band)]\nFranz Ferdinand are a Scottish rock band, formed in 2002 and based in Glasgow.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q855bec4f26",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "I would do so much for people that would do absolutely nothing for me lol at least i know who my true friends are😀",
   "no one does anything for me"
  ]
 },
 {
  "qid": "qeacce5ab81",
  "kind": "yes/no",
  "text": "Tweet: it's funny my mom thinks i possess no remorse when i feel remorse everyday for existing 😎",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qfb444a8077",
  "kind": "yes/no",
  "text": "Claim: Jaap Speyer was born before Bruce Conner.\n\nPassages:\n\n[Jaap Speyer]\nJaap Speyer (1891–1952) was a Dutch film director.\n\n[Bruce Conner]\nBruce Conner (November 18, 1933 – July 7, 2008) was an American artist renowned for his work in assemblage, film, drawing, sculpture, painting, collage, and photography, among other disciplines.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q8d6d6d96e4",
  "kind": "yes/no",
  "text": "Claim: David Nixon and another man are both film directors. The other director directed a film. This film features the song \"Tennessee Homesick Blues\".\n\nPassages:\n\n[Tennessee Homesick Blues]\n\"Tennessee Homesick Blues\" is a song written and recorded by Dolly Parton that was featured in the soundtrack of the 1984 movie \"Rhinestone.\"\n\n[David Nixon (director)]\nDavid Nixon is an American film director and film producer.\n\n[Phil Alden Robinson]\nPhil Alden Robinson (born March 1, 1950) is an American film director and screenwriter whose films include \"Field of Dreams\", \"Sneakers\", and \"The Sum of All Fears\".\n\n[Rhinestone (film)]\nRhinestone is a 1984 American musical comedy film directed by Bob Clark from a screenplay by Sylvester Stallone and Phil Alden Robinson and starring Stallone and Dolly Parton.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q90f0c79f20",
  "kind": "yes/no",
  "text": "Claim: The Football League Super Cup was formed in response to an incident when escaping fans were pressed against a collapsing wall in Heysel Stadium in Brussels in 1986.\n\nPassages:\n\n[Heysel Stadium disaster]\nThe Heysel Stadium disaster (] , ] ; Dutch: \"Heizeldrama\" ; French: \"Drame du Heysel\" ) occurred on 29 May 1985 when escaping fans were pressed against a collapsing wall in the Heysel Stadium in Brussels, Belgium, before the start of the 1985 European Cup Final between Juventus of Italy and Liverpool of England.\n\n[Football League Super Cup]\nThe Football League Super Cup (later known under its sponsored name as the ScreenSport Super Cup) was a one-off football club competition held in England in the 1985–86 season. It was organised by the Football League and was intended as some form of financial and sporting compensation for the English clubs which had qualified for European competition in the previous season but had been banned from entering European tournaments by UEFA following the Heysel Stadium disaster.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qe2e1b9acfd",
  "kind": "yes/no",
  "text": "Claim: The host of the show that featured LA Urban Rangers provided the voice of Backson in the Disney Channel's 51st the Disney Channel animated feature film.\n\nPassages:\n\n[LA Urban Rangers]\nTheir most recent and longest-running outing - the Malibu Public Beach Safari - has been featured in media reports and by Huell Howser on his show.\n\n[Winnie the Pooh (2011 film)]\nIt is the 51st Disney animated feature film.\n\n[Huell Howser]\nHuell Burnley Howser (October 18, 1945 – January 7, 2013) was an American television personality, actor, producer, writer, singer, and voice artist, best known for hosting, producing, and writing \"California's Gold\", his human interest show produced by KCET in Los Angeles for California PBS stations. He also voiced the Backson in \"Winnie the Pooh\" (2011).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qd76d35f0a4",
  "kind": "yes/no",
  "text": "Claim: Cieli di Toscana's singer Bocelli became completely blind at the age of 12.\n\nPassages:\n\n[Cieli di Toscana]\nCieli di Toscana (Tuscan Skies) is Andrea Bocelli's eighth studio album, released in 2001.\n\n[Andrea Bocelli]\nBorn with poor eyesight, Bocelli became completely blind at the age of 12, following a football accident.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q4fcffad6f6",
  "kind": "yes/no",
  "text": "Claim: The producer made his first film under the banner of Excel Entertainment in 2001. He also wrote and produced the film Bangistan. He also produced another film. Kumud Mishra had a role in this other film.\n\nPassages:\n\n[Kumud Mishra]\nHe has had roles in films such as: \"Filmistaan\", \"Revolver Rani\", \"Jolly LLB 2\", \"Raanjhanaa\", \"Badlapur\", \"Bangistan\" and recent Akshay kumar film \"Airlift\" where he played the substantial role of Sanjeev Kohli.\n\n[Ritesh Sidhwani]\nRitesh Sidhwani (born 1973) is a Bollywood film producer, who founded a film production house under the banner of Excel Entertainment Pvt. Ltd. Along with long-time friend Farhan Akhtar, he brought to the audience \"Dil Chahta Hai\", his first film under his banner.\n\n[Dil Chahta Hai]\nDil Chahta Hai (English: \"The Heart Desires\") is a 2001 Indian comedy-drama film starring Aamir Khan, Saif Ali Khan, Akshaye Khanna, Preity Zinta, Sonali Kulkarni, and Dimple Kapadia.\n\n[Bangistan]\nBangistan is a 2015 Bollywood comedy satire film directed by Karan Anshuman and produced by Farhan Akhtar and Ritesh Sidhwani starring Riteish Deshmukh, Pulkit Samrat and Chandan Roy Sanyal in lead roles.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1b1da72fa7",
  "kind": "yes/no",
  "text": "Claim: The man who was portrayed on television by the star of The Fifth Missile served in the U.S. military.\n\nPassages:\n\n[Robert Conrad]\nHe portrayed World War II ace Pappy Boyington in the television series \"Baa Baa Black Sheep\" (later syndicated as \"Black Sheep Squadron\").\n\n[The Fifth Missile]\nThe Fifth Missile is a 1986 TV movie starring Robert Conrad, Sam Waterston and David Soul about an American ballistic missile submarine, based on the novel \"The Gold Crew\" by Frank M. Robinson and Thomas N. Scortia.\n\n[Pappy Boyington]\nGregory \"Pappy\" Boyington (December 4, 1912 – January 11, 1988) was an American combat pilot who was a United States Marine Corps fighter ace during World War II.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q45dc42a4aa",
  "kind": "yes/no",
  "text": "Claim: The band, which released the album \"Gala\", and P.O.D. both consist of four band members.\n\nPassages:\n\n[Lush (band)]\nLush were an English rock band formed in London in 1987. The lineup before the original split consisted of Miki Berenyi (vocals, guitar), Emma Anderson (vocals, guitar), Phil King (bass) and Chris Acland (drums).\n\n[P.O.D.]\nPayable on Death (abbreviated P.O.D.) is a Christian nu metal band formed in 1992 and based in San Diego, California. The band's line-up consists of vocalist Sonny Sandoval, drummer Wuv Bernardo, guitarist Marcos Curiel, and bassist Traa Daniels.\n\n[Gala (album)]\nGala is the debut compilation album by the English alternative rock band Lush, released in 1990 by 4AD as an introduction to the US and Japanese markets, comprising the band's earliest releases in reverse chronological order, plus two additional tracks.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qcfe16b797e",
  "kind": "yes/no",
  "text": "Claim: The director of Daughters of Mara's first album is the son of the producer who worked for the group that evolved from The Iveys. Best! (Jellyfish album) which was released in 1993, did a live cover of a song from this other group.\n\nPassages:\n\n[Badfinger]\nThe band evolved from an earlier group called The Iveys that was formed in 1961 by Ham, Ron Griffiths and David \"Dai\" Jenkins in Swansea, Wales.\n\n[Best! (Jellyfish album)]\nThe song \"No Matter What\" is a live cover of a Badfinger song.\n\n[Daughters of Mara]\nDaughters Of Mara's first album, I Am Destroyer, was produced by Garth Richardson (Mudvayne, Rage Against The Machine) and was released on Virgin Records.\n\n[Garth Richardson]\nHe is the son of Canadian music producer Jack Richardson (whose credits include Alice Cooper, The Guess Who, Badfinger and Poco).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7fe8301ed8",
  "kind": "yes/no",
  "text": "Claim: The morning newspaper, for which Lajos Magyar worked on the staff of, and Stiffelio are not both operas.\n\nPassages:\n\n[Lajos Magyar]\nIn 1922 Magyar went to the Soviet Union as the result of an exchange of prisoners; there he worked on the staff of the Comintern and at the newspaper Pravda.\n\n[Stiffelio]\nStiffelio is an opera in three acts by Giuseppe Verdi, from an Italian libretto by Francesco Maria Piave.\n\n[Pravda]\nPravda (Russian: Правда ; ] , \"Truth\") is a Russian broadsheet newspaper, formerly the official newspaper of the Communist Party of the Soviet Union, when it was one of the most influential papers in the country with a circulation of 11 million.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa1010f61dd",
  "kind": "yes/no",
  "text": "Tweet: I’ve been laid off !! Nice:))",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qeccbb6334b",
  "kind": "yes/no",
  "text": "Tweet: Absolutely prepared to ditch #WoW for #FFXIV at this point...",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qac61a4bc14",
  "kind": "yes/no",
  "text": "Claim: Garry Marshall directed a film. The film costarred the star of the film Open Water 2: Adrift.\n\nPassages:\n\n[Eric Dane]\nAfter appearing in television roles throughout the 2000s such as \"Charmed\", he became known for playing Dr. Mark Sloan on the medical drama television series \"Grey's Anatomy\", as well as films, co-starring in \"Marley & Me\" (2008), \"Valentine's Day\" (2010), and \"Burlesque\" (2010).\n\n[Open Water 2: Adrift]\nPromotional posters claim the film is based on actual events.\n\n[Valentine's Day (2010 film)]\nValentine's Day is a 2010 American romantic comedy film directed by Garry Marshall.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5505610f69",
  "kind": "yes/no",
  "text": "Claim: The winner of the 2014 French Open – Mixed Doubles and another female athlete are both tennis players. This other athlete won the singles title at the 1979 Romika Cup.\n\nPassages:\n\n[Manuel Orantes]\nManuel Orantes Corral (] ; born 6 February 1949) is a former tennis player who was active in the 1970s and 1980s.\n\n[Anna-Lena Grönefeld]\nAnna-Lena Grönefeld (born 4 June 1985) is a German tennis player.\n\n[1979 Romika Cup]\nFirst-seeded Manuel Orantes won the singles title.\n\n[2014 French Open – Mixed Doubles]\nHradecká played alongside Mariusz Fyrstenberg but lost in the second round to the eventual champions Anna-Lena Grönefeld and Jean-Julien Rojer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa9fd64f14a",
  "kind": "yes/no",
  "text": "Claim: The actor Giancarlo Giuseppe Alessandro Esposito who appeared in the 2016 film Money Monster also is best known for his portrayal of Gustavo \"Gus\" Fring on the AMC amc \"Breaking Bad\" and \"Better Call Saul\".\n\nPassages:\n\n[Money Monster]\nMoney Monster is a 2016 American thriller film directed by Jodie Foster and written by Alan Di Fiore, Jim Kouf and Jamie Linden.\n\n[Giancarlo Esposito]\nGiancarlo Giuseppe Alessandro Esposito (born April 26, 1958) is an American actor. He is best known for his portrayal of Gustavo \"Gus\" Fring on the AMC shows \"Breaking Bad\" and \"Better Call Saul\", a role for which he won the Best Supporting Actor in a Drama award at the 2012 Critics' Choice Television Awards and was nominated for an Outstanding Supporting Actor in a Drama Series award at the 2012 Primetime Emmy Awards.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qfd519507bf",
  "kind": "yes/no",
  "text": "Claim: Jeff Ragsdale and Millard Webb are not both authors.\n\nPassages:\n\n[Millard Webb]\nMillard Webb (6 December 1893 – 21 April 1935), was an American screenwriter and director.\n\n[Jeff Ragsdale]\nJeffrey Charles \"Jeff\" Ragsdale ( ) is an American author, documentary filmmaker, actor and stand-up comedian.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q431f49ffb9",
  "kind": "yes/no",
  "text": "Claim: The Dennis Publishing company has published a magazine that Bob Basset has appeared in. Also, a sister publication devoted to the anomalous phenomena popularised by Charles Fort.\n\nPassages:\n\n[Bizarre (magazine)]\nBizarre was a British alternative magazine published from 1997 to 2015. It was published by Dennis Publishing, and was a sister publication to the \"Fortean Times\".\n\n[Bob Basset]\nPublications about Bob Basset appeared in , WAD magazine, VICE UK, Bizarre Magazine, INSIDE artzine magazine.\n\n[Fortean Times]\nFortean Times is a British monthly magazine devoted to the anomalous phenomena popularised by Charles Fort. Previously published by John Brown Publishing (from 1991 to 2001) and then I Feel Good Publishing (2001 to 2005), it is now published by Dennis Publishing Ltd.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qda85d07991",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "When I go to uni Im going to spend more",
   "Can’t wait to be back at uni so I can order more shoes and clothes without my mum telling me off x"
  ]
 },
 {
  "qid": "q3e33ee7e71",
  "kind": "yes/no",
  "text": "Claim: In Search of the Castaways was the Walt Disney production that was based on Jules Verne's 1868 novel \"In Search of the Castaways\". It was not based on the prequel to The Monkey's Uncle.\n\nPassages:\n\n[The Misadventures of Merlin Jones]\nThe Misadventures of Merlin Jones is a 1964 Walt Disney production starring Tommy Kirk and Annette Funicello.\n\n[The Monkey's Uncle]\nThe film is a sequel to the 1964 film \"The Misadventures of Merlin Jones.\"\n\n[In Search of the Castaways (film)]\nIn Search of the Castaways is a 1962 Walt Disney Productions feature film starring Hayley Mills and Maurice Chevalier in a tale about a worldwide search for a shipwrecked sea captain. The film was directed by Robert Stevenson from a screenplay by Lowell S. Hawley based upon Jules Verne's 1868 adventure novel \"Captain Grant's Children\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 }
]
