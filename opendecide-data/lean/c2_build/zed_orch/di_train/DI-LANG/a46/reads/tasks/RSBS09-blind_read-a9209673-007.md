# A46 replay label-noise blind read RSBS09-blind_read-a9209673-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS09-blind_read-a9209673-007.json

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
  "qid": "q4def256033",
  "kind": "yes/no",
  "text": "Claim: Italian Margot Robbie is an actor who won two Logie Award nominations. These were for her portrayal of the character who had an on-off relationship with Ringo Brown.\n\nPassages:\n\n[Donna Freedman]\nDonna Freedman (also Brown) is a fictional character from the Australian soap opera \"Neighbours\", played by Margot Robbie.\n\n[Margot Robbie]\nShe was later cast in the soap opera \"Neighbours\" (2008–2011), which earned her two Logie Award nominations.\n\n[Ringo Brown]\nRingo's storylines have included his ongoing battle with an eating disorder, a bus crash, a relationship with an older woman, the collapse of a warehouse roof at an illegal dance party and his on-off relationship with Donna Freedman.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q64470425db",
  "kind": "yes/no",
  "text": "Text: Turning my head away from the ads that play at the gas pumps as a form of protest",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qb206e624dd",
  "kind": "yes/no",
  "text": "Post: Just signed up for Apple's Ping, told it I like 'classical' and it points me towards Lady Gaga. It takes a certain genius to be this crap.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q7c0a8fffcd",
  "kind": "yes/no",
  "text": "Claim: The series that recounts the adventures of Anne Shirley was published by Scholastic Press in 1908.\n\nPassages:\n\n[Anne of Green Gables]\nAnne of Green Gables is a 1908 novel by Canadian author Lucy Maud Montgomery (published as L. M. Montgomery).\n\n[Twitches (novel series)]\nThe books were published by Scholastic Press, a subsidiary of the Scholastic Corporation, who also published the British Harry Potter series by J.K. Rowling and the Canadian Anne of Green Gables series by Lucy Maud Montgomery.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q07bcd2c0e7",
  "kind": "yes/no",
  "text": "Claim: Shahzeb Khanzada's show \"To The Point\" is written in Urdu.\n\nPassages:\n\n[Express News (Pakistan)]\nExpress News is an Urdu language Pakistani television news channel Based in karachi, launched on January 1, 2008.\n\n[Shahzeb Khanzada]\nHe hosted the talk show \"To The Point\" on Express News from 2011 to 2014 and has hosted the talk show \"Aaj Shahzeb Khanzada Kay Sath\" on Geo News since January 2015.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q99da0a5fd4",
  "kind": "yes/no",
  "text": "Claim: NFL quarterback, Heisman winner, and OU football player graduated from Putnam City North High School.\n\nPassages:\n\n[University of Oklahoma]\nThe University of Oklahoma (OU) is a coeducational public research university in Norman, Oklahoma.\n\n[Sam Bradford]\nBradford attended Putnam City North High School in Oklahoma City, where he starred in football, basketball and golf.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qe85cc9bbe9",
  "kind": "yes/no",
  "text": "Post: What’s in the pollen this year bcos this hayfever is up in my GRILL",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q2332713ede",
  "kind": "yes/no",
  "text": "Claim: Pravda and Stiffelio are not both operas.\n\nPassages:\n\n[Stiffelio]\nStiffelio is an opera in three acts by Giuseppe Verdi, from an Italian libretto by Francesco Maria Piave.\n\n[Pravda]\nPravda (Russian: Правда ; ] , \"Truth\") is a Russian broadsheet newspaper, formerly the official newspaper of the Communist Party of the Soviet Union, when it was one of the most influential papers in the country with a circulation of 11 million.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q075aa48e0d",
  "kind": "yes/no",
  "text": "Claim: George IV was the Prince Regent likely to have stayed in Carlton House in 1811.\n\nPassages:\n\n[Carlton House]\nCarlton House was a mansion in London, best known as the town residence of the Prince Regent for several decades from 1783.\n\n[George IV of the United Kingdom]\nGeorge IV (George Augustus Frederick; 12 August 1762 – 26 June 1830) was King of the United Kingdom of Great Britain and Ireland and of Hanover following the death of his father, George III, on 29 January 1820, until his own death ten years later. From 1811 until his accession, he served as Prince Regent during his father's final mental illness.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q559b68191a",
  "kind": "yes/no",
  "text": "Claim: A song from the Kathy Mattea discography, that peaked at #1 on the Billboard Hot Country Singles & Tracks chart, was first recorded by someone that sang country music.\n\nPassages:\n\n[Don Williams discography]\nThis is a detailed discography for American country music artist Don Williams.\n\n[Come from the Heart]\nIt is most known through the 1989 single by Kathy Mattea, released in conjunction with her album \"Willow in the Wind\", though the song was first recorded and released on the 1987 Don Williams album \"Traces\" and also released in 1988 by Clark's husband on his album \"Old Friends\".\n\n[Kathy Mattea discography]\nOf those Top 10 singles, four of them, \"Goin' Gone\", \"Eighteen Wheels and a Dozen Roses\", \"Come from the Heart\", and \"Burnin' Old Memories\", peaked at #1 on the Billboard Hot Country Singles & Tracks chart.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q38a7cc5a1f",
  "kind": "yes/no",
  "text": "Claim: William Henry Oliphant Smeaton best known work The Hounds of Zaroff was also published as the story that Bloodlust! is based on.\n\nPassages:\n\n[The Most Dangerous Game]\n\"The Most Dangerous Game\", also published as \"The Hounds of Zaroff\", is a short story by Richard Connell, first published in \"Collier's\" on January 19, 1924.\n\n[Seven Faces]\nBased upon the piece of short fiction \"A Friend of Napoleon\" which was published in the June 30, 1923, issue of \"The Saturday Evening Post\" magazine by popular writer Richard Connell (whose best known work, \"The Most Dangerous Game\", was filmed three years later), it was directed by Berthold Viertel and stars Paul Muni in his second screen appearance.\n\n[Bloodlust!]\nis a 1961 American horror thriller film based on Robert Connell's short story \"The Most Dangerous Game.\"",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q929c5bcdb4",
  "kind": "yes/no",
  "text": "Claim: Space Ducks features songs from the band started by Ruben Nielson, who was formerly of the group The Mint Chicks.\n\nPassages:\n\n[Unknown Mortal Orchestra]\nUnknown Mortal Orchestra is an American and New Zealand rock band composed of singer, guitarist and songwriter Ruban Nielson, bassist Jake Portrait, keyboardist Quincy McCrary, and drummer Amber Baker. The band was started by Nielson (formerly of The Mint Chicks).\n\n[Space Ducks]\nIts also features songs from Unknown Mortal Orchestra, Eleanor Friedberger, Deer Tick, Fruit Bats, and Lavender Diamond.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qe7122f5e26",
  "kind": "yes/no",
  "text": "Claim: Matt Vasgersian and Michael Casey are both American.\n\nPassages:\n\n[Matt Vasgersian]\nMatthew Edward \"Matt\" Vasgersian (born September 28, 1967) is an American sportscaster and television host.\n\n[Michael Casey (poet)]\nMichael Casey (born 1947) is an American poet of Armenian descent.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q6567e7054e",
  "kind": "yes/no",
  "text": "Claim: Greg Costikyan did have the same profession as the drummer of the band System of a Down.\n\nPassages:\n\n[John Dolmayan]\nJohn Hovig Dolmayan (Armenian: Ջոն Դոլմայան , born July 15, 1973) is a Lebanese-born Armenian–American songwriter and drummer.\n\n[Greg Costikyan]\nGreg Costikyan (born July 22, 1959, in New York City), sometimes known under the pseudonym \"Designer X\", is an American game designer and science fiction writer.\n\n[System of a Down]\nThe band currently consists of Serj Tankian (lead vocals, keyboards), Daron Malakian (vocals, guitar), Shavo Odadjian (bass, backing vocals) and John Dolmayan (drums).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa320f870e8",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "Donald Trump asked the Chief Medical Officer if people should drink bleach to treat covid 19 and now zoflora, dettol and toilet duck are trending on twitter.",
   "I see Dettol, Toilet Duck and Zoflora are all trending on Twitter. Now why could that be... #TrumpPressBriefing"
  ]
 },
 {
  "qid": "qa470e17fa0",
  "kind": "yes/no",
  "text": "Claim: The 1976 German Grand Prix was won by a driver who retired in 1926.\n\nPassages:\n\n[1976 German Grand Prix]\nThe 14-lap race was the tenth round of the 1976 Formula One season and was won by James Hunt.\n\n[James Hunt]\nAfter retiring from racing in 1979, Hunt became a media commentator and businessman.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qc45b6e5167",
  "kind": "yes/no",
  "text": "Claim: St. Olaf College in America was founded in 1874. It has sent students to the place where Michael E. Bauman was a Lecturer and Tutor in Renaissance theology and Literature for eight years.\n\nPassages:\n\n[Centre for Medieval and Renaissance Studies]\nAmong the American colleges and universities that have sent students to CMRS are The University of Georgia, Elmhurst College, St. Mary's College of California, St. Mary's College of Maryland, St. Olaf College, William Jewell College, Middlebury College.\n\n[St. Olaf College]\nIt was founded in 1874 by a group of Norwegian-American immigrant pastors and farmers, led by Pastor Bernt Julius Muus.\n\n[Michael Bauman]\nHe was for eight years Lecturer and Tutor in Renaissance theology and Literature at the Centre for Medieval and Renaissance Studies, Oxford, where he also was Associate Dean of the Summer School.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q3657f2e2d0",
  "kind": "yes/no",
  "text": "Claim: Ken Howard starred as an attorney in the HBO film Michael Sucsy created.\n\nPassages:\n\n[Grey Gardens (2009 film)]\nGrey Gardens is an HBO film about the lives of Edith Bouvier Beale/\"Little Edie\", played by Drew Barrymore, and her mother Edith Ewing Bouvier/\"Big Edie\", played by Jessica Lange. Co-stars include Jeanne Tripplehorn as Jacqueline Kennedy (Little Edie's cousin) and Ken Howard as Phelan Beale (Little Edie's father).\n\n[Phelan Beale]\nPhelan Beale (May 23, 1881 – June 12, 1956) was an American attorney and sportsman in New York City who was married to Edith Ewing Bouvier, an aunt of Jacqueline Kennedy Onassis.\n\n[Michael Sucsy]\nHe is best known for creating the HBO film \"Grey Gardens\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q6035f7705e",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Elaine Quijano lacks any control in moderating tonight’s debate.",
   "Elaine Quijano exhibits roughly the same amount of control over this debate as two rabbits do on their first date."
  ]
 },
 {
  "qid": "qac68057391",
  "kind": "yes/no",
  "text": "Claim: The song that was scored by the bandmate of O'Neill Spencer, that is often the piece of music played during an evening of revelry, is \"Loch Lomond\".\n\nPassages:\n\n[John Kirby (musician)]\nIn addition to sideman work (prominently with Benny Goodman), Kirby is remembered for leading a successful chamber jazz sextet in the late 1930s and early 1940s, which scored several hit songs including \"Loch Lomond\" and the debut recording of \"Undecided\", a jazz standard.\n\n[O'Neill Spencer]\nHe is most known for his work in the John Kirby Sextet.\n\n[The Bonnie Banks o' Loch Lomond]\nIn Scotland, the song is often the final piece of music played during an evening of revelry (a dance party or dinner, etc.).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qf344ea538e",
  "kind": "yes/no",
  "text": "Claim: The magazine that ranked Lifted Research Group at #5 on its Hot 500 list of fastest-growing companies had a longer lifespan than Optimize.\n\nPassages:\n\n[Lifted Research Group]\nEntrepreneur\" magazine ranked the company at #5 on its 2007 Hot 500 list of fastest-growing companies.\n\n[Entrepreneur (magazine)]\nEntrepreneur is an American magazine and website that carries news stories about entrepreneurship, small business management, and business. The magazine was first published in 1977. The magazine publishes 12 issues annually, available through subscription and on newsstands.\n\n[Optimize (magazine)]\nOptimize was an American monthly business magazine published between November 2001 and June 2007.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2d1f43bbf9",
  "kind": "yes/no",
  "text": "Claim: A five piece band in the \"Art Wave\" scene had the second studio album You Could Have It So Much Better. This band was based in the same city as the band Hey Everyone!.\n\nPassages:\n\n[Art Brut]\nNamed after French painter Jean Dubuffet's definition of outsider art - art by prisoners, loners, the mentally ill, and other marginalized people, and made without thought to imitation or presentation - South London's Art Brut were tagged by \"NME\" as part of the \"Art Wave\" scene that also included bands such as The Rakes, Franz Ferdinand and Bloc Party.\n\n[You Could Have It So Much Better]\nYou Could Have It So Much Better is the second studio album by Scottish indie rock band Franz Ferdinand.\n\n[Hey Everyone!]\nis the debut album by Glasgow-based rock band Dananananaykroyd, released on April 6, 2009, on the Best Before Records label.\n\n[Franz Ferdinand (band)]\nFranz Ferdinand are a Scottish rock band, formed in 2002 and based in Glasgow.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q0263f1531e",
  "kind": "yes/no",
  "text": "Text: Amazing how fast this team can go winning from 13 straight to losing three in a row. Lol. Horrible managing tonight. I really hope this Boone experiment is over soon.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qbca72248f7",
  "kind": "yes/no",
  "text": "Claim: Brad Budde played professionally for a team in the NFL that was founded in 1960 as the Dallas Texans by Lamar Hunt.\n\nPassages:\n\n[Brad Budde]\nHe was a first-round pick in the 1980 NFL Draft, and played professionally for the NFL's Kansas City Chiefs.\n\n[Kansas City Chiefs]\nThe team was founded in 1960 as the Dallas Texans by businessman Lamar Hunt and was a charter member of the American Football League (AFL) (they are not associated with an earlier Dallas Texans NFL team that only played for one season in 1952).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q553567859e",
  "kind": "yes/no",
  "text": "Claim: Mammal, or Mammals, are a class of vertebrates within the class of Mammalia that has at least 2 types of sensors.\n\nPassages:\n\n[Mammal]\nMammals are any vertebrates within the class Mammalia ( from Latin \"mamma\" \"breast\"), a clade of endothermic amniotes distinguished from reptiles (including birds) by the possession of a neocortex (a region of the brain), hair, three middle ear bones, and mammary glands. Females of all mammal species nurse their young with milk, secreted from the mammary glands.\n\n[Thermoception]\nMammals have at least two types of sensor: those that detect heat (i.e., temperatures above body temperature) and those that detect cold (i.e. temperatures below body temperature).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q857fb5d362",
  "kind": "yes/no",
  "text": "Claim: Proud To Commit Commercial Suicide is a live spanish language album by industrial metal band Nailbomb and captures the band's only live appearance at the 1995 Dynamo Open Air Festival, the album cover is a picture of the aftermath of the Jonestown infamous remote settlement established by the Peoples Temple, an American socialist organization under the leadership of Jim Jones, in northwestern Guyana.\n\nPassages:\n\n[Jonestown]\nThe Peoples Temple Agricultural Project, better known by its informal name \"Jonestown\", was a remote settlement established by the Peoples Temple, an American socialist organization under the leadership of Jim Jones, in northwestern Guyana.\n\n[Proud to Commit Commercial Suicide]\nThe album cover is a picture of the aftermath of the infamous Jonestown suicides.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q193c21a7d6",
  "kind": "yes/no",
  "text": "Claim: MindGamers is a 2015 German science fiction film directed by Andrew Goth, the film stars Antonia Campbell-Hughes, a Northern Irish actress and former fashion designer, best known for appearing in Jack Dee's sitcom \"Lead Balloon\".\n\nPassages:\n\n[MindGamers]\nMindGamers is a 2015 Austrian science fiction film directed by Andrew Goth.\n\n[Antonia Campbell-Hughes]\nAntonia Campbell-Hughes (born 7 September 1982) is a Northern Irish actress and former fashion designer, best known for appearing in Jack Dee's sitcom \"Lead Balloon\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q19c09fa91b",
  "kind": "yes/no",
  "text": "Claim: The Sewanhaka Central High School District is composed of Sewanhaka High School, Concordia Junior-Senior High School, New Hyde Park Memorial High School, Floral Park Memorial High School, and one other. That other school serves students in the census-designated place of Nassau County in New York.\n\nPassages:\n\n[H. Frank Carey Junior-Senior High School]\nH. Frank Carey High School is a public high school located in Franklin Square, New York serving students in the seventh through twelfth grades from the towns of Franklin Square, Garden City South, West Hempstead, and Elmont.\n\n[Garden City South, New York]\nGarden City South is a hamlet and census-designated place (CDP) in Nassau County, New York, United States.\n\n[Sewanhaka Central High School District]\nThe district is currently composed of five high schools: Sewanhaka High School, Elmont Memorial High School, New Hyde Park Memorial High School, Floral Park Memorial High School, and H. Frank Carey Junior-Senior High School.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q25a0cafd12",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "They really took friends off Netflix 😭😩🤦🏼‍♀️ what am I suppose to watch now??!??!!",
   "I dislike that they took friends off Netflix, I enjoy watching the show"
  ]
 },
 {
  "qid": "q53cd208fbf",
  "kind": "yes/no",
  "text": "Claim: The creator of the character, for whom Helena Štáchováwas provided the Czech-language voice of, was born in July, 1954.\n\nPassages:\n\n[Helena Štáchová]\nNotably, Štáchová provided the Czech language-voice of Lisa Simpson on the Czech version of the American animated sitcom, \"The Simpsons\".\n\n[Matt Groening]\nMatthew Abraham \"Matt\" Groening ( ; born February 15, 1954) is an American cartoonist, writer, producer, animator, and voice actor.\n\n[Lisa Simpson]\nCartoonist Matt Groening created and designed her while waiting to meet James L. Brooks.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q71b4941e22",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "eurovision belongs to everyone!",
   "so many people pressed that italy won sorry eurovision belongs to the bisexuals now x #Eurovision"
  ]
 },
 {
  "qid": "q29f39ae0ef",
  "kind": "yes/no",
  "text": "Claim: The English Egyptologist that excavated the pyramid Harageh is known mainly for his works in the Egyptian Museum that is named after the capital of Egypt.\n\nPassages:\n\n[Reginald Engelbach]\nReginald Engelbach (July 9, 1888 – February 26, 1946) was an English Egyptologist and engineer. He is mainly known for his works in the Egyptian Museum of Cairo, above all the compilation of a register of artifacts belonging of the museum.\n\n[Harageh]\nReginald Engelbach excavated these cemeteries in 1913.\n\n[Cairo]\nCairo ( ; Arabic: القاهرة‎ ‎ \"al-Qāhirah \", , Coptic: \"Kahire \") is the capital and largest city of Egypt.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q52fd88de35",
  "kind": "yes/no",
  "text": "Claim: The puzzle compendium \"Fires of Winter\" reached the \"New York Times\" bestseller list.\n\nPassages:\n\n[Fires of Winter]\nFires of Winter is a novel by Johanna Lindsey originally published in September 1980 by Avon Books.\n\n[Johanna Lindsey]\nJohanna Lindsey (born Johanna Helen Howard, March 10, 1952), is one of the most popular American writers of historical romance novels worldwide. All of her books reached the \"New York Times\" bestseller list, many reaching No. 1.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q54b5dd569d",
  "kind": "yes/no",
  "text": "Claim: \"Get Stoned\" is a song by a Californian rock band. The Fatima Mansions rock band was formed earlier than this band.\n\nPassages:\n\n[Get Stoned]\n\"Get Stoned\" is a song by American rock band Hinder.\n\n[The Fatima Mansions]\nThe Fatima Mansions were an art rock group formed in 1988 by Cork singer/keyboardist Cathal Coughlan, formerly of Microdisney.\n\n[Hinder]\nHinder is an American rock band from Oklahoma that was formed in 2001 by lead singer Austin Winkler, lead guitarist Joe \"Blower\" Garvey, and drummer Cody Hanson.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2ed665df74",
  "kind": "yes/no",
  "text": "Claim: The larval food plant of Leto venus is found on the same western continent as Cyrtolabulus. Koeleria, however, is found all over.\n\nPassages:\n\n[Leto venus]\nThe larval food plant is \"Virgilia\".\n\n[Virgilia (plant)]\nVirgilia is a genus of Southern African trees in the family Fabaceae, having shiny to hairy pinnate leaves and attractive mauve to pink pea-shaped flowers followed by leathery pods.\n\n[Cyrtolabulus]\nCyrtolabulus is an African, Indomalayan and Palearctic genus of potter wasps.\n\n[Koeleria]\nKoeleria is a common and widespread genus of plants in the grass family, found on all continents except Antarctica and on various oceanic islands.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q8839a81e2e",
  "kind": "yes/no",
  "text": "Claim: Robert Weissberg is a political scientist and author. The magazine he writes for ranked the company, headquartered at the Port Plaza Mall, as number 81 in 2016.\n\nPassages:\n\n[Schreiber Foods]\nWith more than $5 billion in annual sales, Forbes ranked Schreiber Foods as the 81st largest private employer in 2016.\n\n[Port Plaza Mall]\nThe mall property was razed during the 1st half of 2012 as part of a redevelopment project; the headquarters of Schreiber Foods now stands on the main mall footprint.\n\n[Robert Weissberg]\nWeissberg has also written for magazines such as \"Forbes,\" \"Society\", and \"The Weekly Standard\".\n\n[Forbes]\nPublished bi-weekly, it features original articles on finance, industry, investing, and marketing topics.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q019e26ea36",
  "kind": "yes/no",
  "text": "Claim: The genus closely related to Bignonia and Pithecoctenium is a genus of flowering plants. The genus with the same name as one of Diogenes of Athens (tragedian) works is not.\n\nPassages:\n\n[Diogenes of Athens (tragedian)]\nHis works are listed by the Suda as \"Semele\", \"Achilles, Helen, Herakles, Thyestes, Medea, Oedipus,\" and \"Chrysippus\".\n\n[Semele]\nSemele ( ; Greek: Σεμέλη \"Semelē\"), in Greek mythology, daughter of the Boeotian hero Cadmus and Harmonia, was the mortal mother of Dionysus by Zeus in one of his many origin myths.\n\n[Pithecoctenium]\nThe genus is closely related to \"Bignonia\" and \"Anemopaegma\".\n\n[Anemopaegma]\nAnemopaegma is a genus of flowering plants in the family Bignoniaceae.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe90c57a541",
  "kind": "yes/no",
  "text": "Claim: The genus that Clianthus maximus belongs in, has more flower species than Callicoma.\n\nPassages:\n\n[Clianthus]\nClianthus, commonly known as kakabeak (\"Kōwhai ngutukākā\" in Māori), is a genus of flowering plants in the legume family Fabaceae, comprising two species of shrubs native to New Zealand.\n\n[Clianthus maximus]\nIt is one of two species of \"Clianthus\" (kaka beak) and both have striking clusters of red flowers which resemble the beak of the kākā, a New Zealand parrot.\n\n[Callicoma]\nCallicoma, is a plant genus that contains just one species, Callicoma serratifolia, a tall shrub or small tree which is native to Australia.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe8d7c72ae3",
  "kind": "yes/no",
  "text": "Claim: The composer of Kamarinskaya is not the same nationality as another composer. This composer wrote the opera \"I puritani\"\n\nPassages:\n\n[Vincenzo Bellini]\nVincenzo Salvatore Carmelo Francesco Bellini (] ; 3 November 1801 – 23 September 1835) was an Italian opera composer, who was known for his long-flowing melodic lines for which he was named \"the Swan of Catania\".\n\n[I puritani]\nI puritani (\"The Puritans\") is an opera in by Vincenzo Bellini.\n\n[Kamarinskaya]\nKamarinskaya (Russian: камаринская ) is a Russian traditional folk dance, which is mostly known today as the Russian composer Mikhail Glinka's composition of the same name.\n\n[Mikhail Glinka]\nMikhail Ivanovich Glinka (Russian: Михаи́л Ива́нович Гли́нка ; 1 June [O.S. 20 May] 1804 15 February [O.S. 3 February] 1857 ) was the first Russian composer to gain wide recognition within his own country, and is often regarded as the fountainhead of Russian classical music.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qa6a0bcefb3",
  "kind": "yes/no",
  "text": "Claim: Greenwich House is the historic meeting venue built in a style taught at the Ecole des Beaux-Arts.\n\nPassages:\n\n[Dayton Memorial Hall]\nThe Dayton Memorial Hall is a historic meeting venue on First Street in downtown Dayton, Ohio, United States. Constructed shortly after the turn of the twentieth century, this Beaux-Arts structure is one of many memorial halls statewide from the same time period, and it has been named a historic site.\n\n[Beaux-Arts architecture]\nBeaux-Arts architecture ( ; ] ) expresses the academic neoclassical architectural style taught at the \"École des Beaux-Arts\" in Paris.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q205c5f3fe7",
  "kind": "yes/no",
  "text": "Claim: A number of Carmen Robertson's writings focus on this Aboriginal Canadian artist. Which is the Aboriginal Canadian artist of the M'Chigeeng.\n\nPassages:\n\n[Norval Morrisseau]\nNorval Morrisseau, CM (March 14, 1932 – December 4, 2007), also known as Copper Thunderbird, was an Aboriginal Canadian artist.\n\n[Carmen Robertson]\nA number of Robertson's writings focus on the Aboriginal Canadian artist Norval Morrisseau.\n\n[Blake Debassige]\nBlake Debassige is a Native Canadian artist of the M'Chigeeng First Nation, born at West Bay on Manitoulin Island in Ontario on June 22, 1956.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc7d55222a5",
  "kind": "yes/no",
  "text": "Claim: Billy Idol is older than the Australian singer-songwriter who co-wrote \"Love No Limit\" with Dave Hall.\n\nPassages:\n\n[Billy Idol]\nWilliam Michael Albert Broad (born 30 November 1955), known professionally as Billy Idol, is an English musician, singer, songwriter, and actor.\n\n[Kenny Greene]\nKenny Greene (January 17, 1969 – October 1, 2001) was an American singer-songwriter who was also a member of the R&B group Intro.\n\n[Love No Limit]\nIt was co-written by Kenny Greene and Dave Hall for her debut album, \"What's the 411?",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q64977240c1",
  "kind": "yes/no",
  "text": "Claim: The King that Gothard Wilhelm Butler was captain of the guard for was known by the name Jan Kazimierz in Poland.\n\nPassages:\n\n[John II Casimir Vasa]\nIn Poland, he is known and commonly referred as Jan Kazimierz.\n\n[Gothard Wilhelm Butler]\nHe was Grand treasurer of the Crown, the Crown court chamberlain and a captain of the guard of King John II Casimir Vasa and erderman of Prienai, Parnu and Bolesław.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q78cb5d7eee",
  "kind": "yes/no",
  "text": "Text: How DARE my friends have jobs/boyfriends/lives they should consider my feelings and be free when I am",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qc4c02aec7b",
  "kind": "yes/no",
  "text": "Claim: Timothy Simon \"Tim\" Roth gained recognition earlier than the mother of a Nickelodeon duo. Boris Pelekh worked with this duo from 2008 - 2011.\n\nPassages:\n\n[Nat and Alex Wolff]\nThe siblings are known for their work on the Nickelodeon television series \"The Naked Brothers Band\", which was created and produced by their mother, actress Polly Draper.\n\n[Tim Roth]\nTimothy Simon \"Tim\" Roth (born 14 May 1961) is an English actor and director. He garnered critical acclaim for his role as Myron in the 1984 film \"The Hit\" (1984), for which he was nominated for his first BAFTA Award.\n\n[Boris Pelekh]\nAside from his work in Gogol Bordello, he also worked with the Nickelodeon duo Nat and Alex Wolff from 2008 - 2011.\n\n[Polly Draper]\nShe first gained recognition for her role in the ABC primetime television drama \"Thirtysomething\" (1987–91).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q5cb8687fa8",
  "kind": "yes/no",
  "text": "Claim: Ben R. Guttery was the reporter who reflected on the contrast between Ethiopian Airlines and other African Airlines.\n\nPassages:\n\n[Airlines of Africa]\nBen R. Guttery, author of \"Encyclopedia of African Airlines\", said \"Although most of the carriers have never been large by European or American standards, they have had tremendous impact on the economy and the people.\"\n\n[Ethiopian Airlines accidents and incidents]\nEthiopian Airlines, the national airline of Ethiopia, has a good safety record, by contrast to other African airlines.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe763359d54",
  "kind": "yes/no",
  "text": "Claim: Ivan \"John\" Jurkovic played for the Cleveland Browns, a professional American football team based in Ohio.\n\nPassages:\n\n[Cleveland Browns]\nThe Cleveland Browns are a professional American football team based in Cleveland, Ohio.\n\n[John Jurkovic]\nIvan \"John\" Jurkovic (born August 18, 1967) is a former American football player currently employed as a broadcaster. Jurkovic played professionally as a defensive tackle for the Green Bay Packers, Jacksonville Jaguars, and Cleveland Browns.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q94d271e14e",
  "kind": "yes/no",
  "text": "Claim: The Scadoxus plant not which Enkianthus campanulatus is the hardiest species to be small enough. This plant could to be grown as an ornamental plant in tiny containers.\n\nPassages:\n\n[Scadoxus]\nSpecies of \"Scadoxus\" are grown as ornamental plants for their brilliantly coloured flowers, either in containers or in the ground in frost-free climates.\n\n[Enkianthus campanulatus]\nThe hardiest of \"Enkianthus\" species is E. campanulatus (furin-tsutsuji or redvein enkianthus), a medium-sized, narrow, upright, deciduous shrub.\n\n[Enkianthus]\nEnkianthus is a genus of shrubs or small trees in the heath family (Ericaceae).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe22c9eb5d9",
  "kind": "yes/no",
  "text": "Claim: This One's for the Children had lead vocals by an American singer and songwriter.\n\nPassages:\n\n[This One's for the Children]\nThe lead vocals were sung by Jordan Knight and Donnie Wahlberg.\n\n[Donnie Wahlberg]\nDonald Edmond Wahlberg Jr. (born August 17, 1969) is an American singer, songwriter, actor, record producer, and film producer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q17ffb3a97e",
  "kind": "yes/no",
  "text": "Claim: The Seattle Fighter Wing was a unit of the United States Air Force, active during the Pacific War of 1941-45, it was based in the Northwestern United States in Washington state.\n\nPassages:\n\n[Northwestern United States]\nThe Northwestern United States is an informal geographic region of the United States.\n\n[Seattle Fighter Wing]\nThe Seattle Fighter Wing was a unit of the United States Air Force, active during the Pacific War of 1942-45.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 }
]
