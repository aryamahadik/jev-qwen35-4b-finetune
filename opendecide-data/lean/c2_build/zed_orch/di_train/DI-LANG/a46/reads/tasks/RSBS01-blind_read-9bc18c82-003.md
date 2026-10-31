# A46 replay label-noise blind read RSBS01-blind_read-9bc18c82-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS01-blind_read-9bc18c82-003.json

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
  "qid": "qea17d5145f",
  "kind": "yes/no",
  "text": "Claim: The IRA used a Barrack buster to shoot down a British Army Lynx helicopter.\n\nPassages:\n\n[Barrack buster]\nBarrack buster is the colloquial name given to several improvised mortars, developed in the 1990s by the engineering group of the Provisional Irish Republican Army (IRA).\n\n[1994 British Army Lynx shootdown]\nOn 20 March 1994, a British Army Lynx helicopter was shot down by the Provisional Irish Republican Army (IRA) in Northern Ireland.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q741789606e",
  "kind": "yes/no",
  "text": "Claim: A Pottawatomie massacre event known was Bleeding Kansas was largely brought about by the Missouri Compromise and the act which created the terrirtories of Kansas and Nebraska and was combated by the Republican Party.\n\nPassages:\n\n[History of the United States Republican Party]\nThe Republican Party, also commonly called the GOP (for \"Grand Old Party\"), is one of the world's oldest extant political parties. It emerged in 1854 to combat the Kansas–Nebraska Act, an act that dissolved the terms of the Missouri Compromise and allowed slave or free status to be decided in the territories by popular sovereignty.\n\n[Kansas–Nebraska Act]\n277 ) created the territories of Kansas and Nebraska and was drafted by Democratic Senator Stephen A. Douglas of Illinois and President Franklin Pierce.\n\n[Pottawatomie massacre]\nBleeding Kansas was largely brought about by the Missouri Compromise and the Kansas–Nebraska Act.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qbd0662aa74",
  "kind": "yes/no",
  "text": "Claim: Jonghyun was a member of the boy group Shinee who released their first studio album \"She is\".\n\nPassages:\n\n[Kim Jong-hyun (singer)]\nHe is a vocalist of the South Korean boy group Shinee, and has further participated in S.M. Entertainment's project group S.M.\n\n[She Is]\nShe Is (Hangul: 좋아 ; RR: \"Joh ah \" \"good\") is the first studio album by South Korean singer-songwriter Jonghyun, released on May 24, 2016 by S.M. Entertainment and distributed by KT Music.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qba15623da9",
  "kind": "yes/no",
  "text": "Claim: El Paso International Airport is further from their town than Grand Forks International.\n\nPassages:\n\n[El Paso International Airport]\nEl Paso International Airport (IATA: ELP, ICAO: KELP, FAA LID: ELP) is a public airport four miles (6 km) northeast of downtown El Paso, in El Paso County, Texas, United States.\n\n[Grand Forks International Airport]\nGrand Forks International Airport (IATA: GFK, ICAO: KGFK, FAA LID: GFK) is a public airport five miles (8 km) northwest of Grand Forks, in Grand Forks County, North Dakota.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qe9e2f64009",
  "kind": "yes/no",
  "text": "Tweet: Just rediscovered that my nose is always in my field of vision so I will unfortunately be dropping out as I cannot continue my assigned readings in peace",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qb016114b23",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Dear @krispykremeUK, I note your #Thanksgiving offer that ends on 2 Dec. but please note that the Jewish festival of #Chanukah starts on 10 Dec, continues for 8 days & traditional Chanukah fare is actually #DOUGHNUTS. Please consider a special offer for this, too.",
   "Dear @krispykremeUK, I see your enticing #Thanksgiving offer that ends on 2 Dec. I wanted to ask if you're aware that #Chanukah starts on 10 Dec, continues for 8 days &amp; that traditional Chanukah fare is actually #DOUGHNUTS ?? 🍩🍩 #justsaying #AskingForAFriend #opportunity"
  ]
 },
 {
  "qid": "q894525dda1",
  "kind": "yes/no",
  "text": "Claim: The head coach for the 2012 Columbia Lions football team is American. As is the individual that Jerry York (businessman) was chief aide to.\n\nPassages:\n\n[2012 Columbia Lions football team]\nThey were led by first year head coach Pete Mangurian and played their home games at Robert K. Kraft Field at Lawrence A. Wien Stadium.\n\n[Jerry York (businessman)]\nHe was a chief aide to Kirk Kerkorian and his Tracinda investment company.\n\n[Pete Mangurian]\nPeter K. Mangurian born June 17, 1955 is an American football coach and former player.\n\n[Kirk Kerkorian]\nKerkor \"Kirk\" Kerkorian (June 6, 1917 – June 15, 2015) was an Armenian-American businessman, investor, and philanthropist.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q9d136e337f",
  "kind": "yes/no",
  "text": "Claim: The city where radio personality Ye Sha is from has a higher population than this place. It is where Zhu Shaolian was born.\n\nPassages:\n\n[Hengyang]\nIts built-up (\"or metro\") area made of 4 out of 5 urban districts was home to 1,075,516 inhabitants at the 2010 census.\n\n[Ye Sha]\nYe Sha (Chinese: 叶 沙, Hanyu Pinyin: \"Yè Shā\") is a radio personality from Shanghai, China.\n\n[Shanghai]\nShanghai is one of the four direct-controlled municipalities of China and the most populous city proper in the world with a population of more than 24 million as of 2014 .\n\n[Zhu Shaolian]\nBorn in Hengyang, Hunan Province, Zhu joined the Communist Youth League of China in 1921 and the Communist Party of China in February 1922.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q620b3da67e",
  "kind": "yes/no",
  "text": "Claim: The Tama Maru No. 2 was damaged by this World War II American naval scout plane and dive bomber, which was manufactured by Douglas Aircraft. This plane was replaced by Curtiss SB2C Helldiver.\n\nPassages:\n\n[Japanese minesweeper Tama Maru No. 2]\nOn 10 March 1942, during the invasion of Lae-Salamaua, \"Tama Maru No. 2\" was damaged by Douglas SBD Dauntless dive bombers from the United States Navy aircraft carriers USS \"Lexington\" and USS \"Yorktown\" off Lae, New Guinea.\n\n[Curtiss SB2C Helldiver]\nIt replaced the Douglas SBD Dauntless in US Navy service.\n\n[Douglas SBD Dauntless]\nThe Douglas SBD Dauntless was a World War II American naval scout plane and dive bomber that was manufactured by Douglas Aircraft from 1940 through 1944.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q565f9e2e20",
  "kind": "yes/no",
  "text": "Claim: Melanie Hamilton Wilkes is a fictional character first appearing in a novel whose story is set during the American Civil War and is about two lesbian lovers.\n\nPassages:\n\n[Melanie Hamilton]\nMelanie Hamilton Wilkes is a fictional character first appearing in the novel \"Gone with the Wind\" by Margaret Mitchell.\n\n[Gone with the Wind (novel)]\nGone with the Wind is a novel by American writer Margaret Mitchell, first published in 1936. The story is set in Clayton County and Atlanta, both in Georgia, during the American Civil War and Reconstruction Era.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q5a0f2a07b7",
  "kind": "yes/no",
  "text": "Claim: Produced by the prominent music make,r Celabraison is the debut album by Sleeper Agent. The same producer released Thank You, Happy Birthday.\n\nPassages:\n\n[Celabrasion]\nCelabraison is the debut album by American rock band Sleeper Agent. The album was produced by Jay Joyce and released digitally on iTunes on August 2, 2011 via Mom + Pop Music and physically on September 27, 2011.\n\n[Jay Joyce]\nJohn Joseph \"Jay\" Joyce is an American record producer, songwriter and session musician.\n\n[Thank You, Happy Birthday]\nThe album was produced by Jay Joyce, who worked in the same capacity on the band's eponymous debut album.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8600afcdf0",
  "kind": "yes/no",
  "text": "Claim: The band that recorded Shapes (album), not the band that recorded The Big Come Up, is an American rock band. They originated from Chapel Hill, North Carolina.\n\nPassages:\n\n[Shapes (album)]\nShapes is Polvo's fourth studio album.\n\n[The Black Keys]\nThe Black Keys are an American rock band formed in Akron, Ohio, in 2001.\n\n[The Big Come Up]\nThe Big Come Up is the debut studio album by the American rock duo The Black Keys, released in 2002 on Alive Records.\n\n[Polvo]\nPolvo is an American indie noise rock band from Chapel Hill, North Carolina.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q23fdf5e99e",
  "kind": "yes/no",
  "text": "Claim: Light quadricycles (L6e), and electric quadricycles (L7e) are the two categories of the non-electric version of the neighbourhood electric bike.\n\nPassages:\n\n[Motorised quadricycle]\nTwo categories are defined; knowingly light quadricycles (L6e), and heavy quadricycles (L7e).\n\n[Neighborhood Electric Vehicle]\nThe non-electric version of the neighbourhood electric vehicle is the Motorised quadricycle.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf1ddc22768",
  "kind": "yes/no",
  "text": "Claim: The artist created the 'Beguiling of Merlin' and was closely associated with the later part of the Pre-Raphaelite movement. He also painted the Pygmalion and the Image series.\n\nPassages:\n\n[Edward Burne-Jones]\nSir Edward Coley Burne-Jones, 1st Baronet {'1': \", '2': \", '3': \", '4': \"} (28 August 183317 June 1898) was a British artist and designer closely associated with the later phase of the Pre-Raphaelite movement, who worked closely with William Morris on a wide range of decorative arts as a founding partner in Morris, Marshall, Faulkner & Co.\n\n[The Beguiling of Merlin]\nThe Beguiling of Merlin is a painting by the Pre-Raphaelite painter Edward Burne-Jones which was created between 1872 and 1877.\n\n[Pygmalion and the Image series]\nPygmalion and the Image is the second series of four oil paintings in the Pygmalion and Galatea series by the Pre-Raphaelite artist Edward Burne-Jones which was completed between 1875 and 1878.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q2d4d9ae204",
  "kind": "yes/no",
  "text": "Claim: Spaniard César Vallejo was not a German national. Neither was the author of Tales of a Long Night.\n\nPassages:\n\n[Alfred Döblin]\nBruno Alfred Döblin (10 August 1878 – 26 June 1957) was a German novelist, essayist, and doctor, best known for his novel \"Berlin Alexanderplatz\" (1929).\n\n[Tales of a Long Night]\nTales of a Long Night (German: \"Hamlet oder Die lange Nacht nimmt ein Ende\" ) (1956) is the last novel of German author Alfred Döblin.\n\n[César Vallejo]\nCésar Abraham Vallejo Mendoza (March 16, 1892 – April 15, 1938) was a Peruvian poet, writer, playwright, and journalist.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6489f3e0fa",
  "kind": "yes/no",
  "text": "Claim: The actress who starred in The Legend of the Blue Sea, rose to fame after her as a girl in a film that's title means \"That Bizarre Girl\".\n\nPassages:\n\n[My Sassy Girl]\nMy Sassy Girl (Korean: 엽기적인 그녀 ; literally, \"That Bizarre Girl\") is a 2001 South Korean romantic comedy film directed by Kwak Jae-yong, starring Jun Ji-hyun and Cha Tae-hyun.\n\n[The Legend of the Blue Sea]\nThe Legend of the Blue Sea () is a 2016-2017 South Korean television series starring Jun Ji-hyun and Lee Min-ho.\n\n[Jun Ji-hyun]\nJun Ji-hyun (born Wang Ji-hyun on 30 October 1981), also known as Gianna Jun, is a South Korean actress. She rose to fame for her role as The Girl in the romantic comedy \"My Sassy Girl\" (2001), one of the highest-grossing Korean comedies of all time.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa4d2dcad7f",
  "kind": "yes/no",
  "text": "Claim: The twin brother of Greek mathematician Scholastica is the patron saint of Europe, and has a historical religious building in Castres, Languedoc, France named after him.\n\nPassages:\n\n[Castres Cathedral]\nCastres Cathedral (\"Cathédrale Saint-Benoît de Castres\"), now the Roman Catholic church of Saint Benoît (Saint Benedict), is a historical religious building in Castres, Languedoc, France.\n\n[Scholastica]\nBorn in Italy, according to a ninth century tradition, she was the twin sister of Benedict of Nursia.\n\n[Benedict of Nursia]\nBenedict of Nursia (Latin: \"Benedictus de Nursia\" ; Italian: \"Benedetto da Norcia\" ; Vulgar Latin: \"*Benedecto\"; Gothic: \"𐌱𐌴𐌽𐌴𐌳𐌹𐌺𐍄, Benedikt\" ; 2 March 480 – 543 or 547 AD) is a Christian saint, who is venerated in the <a href=\"Eastern%20Orthodox%20Church\">Eastern Orthodox Church</a>es, the <a href=\"Catholic%20Church\">Catholic Church</a>, the <a href=\"Oriental%20Orthodoxy\">Oriental Orthodox Churchese <a href=\"Anglican%20Communion\">Anglican Communion</a> and <a href=\"Old%20Catholic%20Church\">Old Catholic Church</a>es. He is a patron saint of Europe.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qb969ef2a03",
  "kind": "yes/no",
  "text": "Claim: The animal breed that is a cousin of the German longhaired pointer was developed in Germany and not the Bracco Italiano.\n\nPassages:\n\n[Large Münsterländer]\nThe Large Münsterländer (or Großer Münsterländer) is a breed of gun dog originally from the Münster region in Germany.\n\n[Bracco Italiano]\nThe Bracco Italiano ] is a breed of dog developed in Italy as a versatile gun dog.\n\n[German Longhaired Pointer]\nIt is closely related to its cousins, the German Shorthaired Pointer (GSP), the German Wirehaired Pointer (GWP) and the Large Münsterländer, which was previously part of the breed.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q0afcdf85eb",
  "kind": "yes/no",
  "text": "Claim: Joseph Smith founded Methodism along with the man who was also part of the revival movement in England and the Great Awakening in the United States.\n\nPassages:\n\n[John Wesley]\nJohn Wesley ( or ; 28 June [O.S. 17 June] 1703 2 March 1791) was an English Anglican cleric and theologian who, with his brother Charles and fellow cleric George Whitefield, founded Methodism.\n\n[United Methodist Church]\nThe UMC traces its roots back to the revival movement of John and Charles Wesley in England as well as the Great Awakening in the United States.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q08e61a712c",
  "kind": "yes/no",
  "text": "Claim: The musician that released 1995's Made in Sea is a vocalist. So is the singer and songwriter who released the album \"I en tid som vår\".\n\nPassages:\n\n[I en tid som vår]\nI en tid som vår \"(In a time like ours)\" is the fifth album from Swedish pop singer and songwriter Marie Fredriksson.\n\n[Made in Sea]\nMade In Sea is a third album released in January 26, 2006 by South Korean singer Bada.\n\n[Marie Fredriksson]\nGun-Marie Fredriksson, known as (born 30 May 1958), is a Swedish pop singer-songwriter and pianist, best known for forming one half of the pop rock duo Roxette, which she created together with Per Gessle in 1986.\n\n[Bada (singer)]\nChoi Sung-hee (born February 28, 1980), better known as Bada or Sea, is a South Korean singer and musical actress.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qbf377ac813",
  "kind": "yes/no",
  "text": "Post: 2021 is for your washer and dryer just becoming one appliance",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q5c7b73329a",
  "kind": "yes/no",
  "text": "Claim: The writer of the songs in All We Know Is Falling is younger than the lead singer of heavy metal band CWHL. I Am the Night was also the last album to feature this lead singer.\n\nPassages:\n\n[I Am the Night]\nIt was also the last album to feature lead singer Terry Glaze.\n\n[All We Know Is Falling]\nAll songs were written by vocalist Hayley Williams and guitarist Josh Farro.\n\n[Hayley Williams]\nHayley Nichole Williams (born December 27, 1988) is an American singer, songwriter and musician. The band consists of Hayley Williams, Zac Farro and Taylor York.\n\n[Terry Glaze]\nTerrence Lee Glaze (born November 29, 1964, Columbus), known as Terry Lee, is a Texas-raised singer and guitarist who is most known for his work in American heavy metal bands Lord Tracy and Pantera.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qe324889417",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I really do not love hurting my foot, it's really painful!",
   "I hurt my foot like 3 days ago, I have no idea how, but it hurts to put pressure on it. Love that for me"
  ]
 },
 {
  "qid": "q4a16dcdca7",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "So our landlord just brought in new sofas which is lovely but in the process broke a table, someone’s cup and spilt tea on the carpet and left saying “you should probably clean that up” thanks Darren 🖕🏼",
   "Exact same tweet but at the end, saying \"fuck you Darren\""
  ]
 },
 {
  "qid": "q42ef80c3e7",
  "kind": "yes/no",
  "text": "Claim: The nationality of the stage costume designer of Homage to the Queen was English.\n\nPassages:\n\n[Homage to the Queen]\nHomage to the Queen, Op. 42, by Malcolm Arnold was written as the official coronation ballet in 1953, commissioned by the Sadler's Wells Ballet in honour of Queen Elizabeth II, the ballet company's musical adviser Humphrey Searle having recommended Arnold for the job. It was first performed by the Sadler's Wells Ballet on Coronation night 2 June 1953 at the Royal Opera House Covent Garden, with original scenery and costumes by Oliver Messel.\n\n[Oliver Messel]\nOliver Hilary Sambourne Messel (13 January 1904 – 13 July 1978) was an English artist and one of the foremost stage designers of the 20th century.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q141c570930",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "My roommate has no redeeming qualities",
   "I've made a roommate complain tweet every day, and he's done another thing, but I'm tired of negativity so I'm gonna list all the things I like about him! Here they are:"
  ]
 },
 {
  "qid": "qbb9e5783ac",
  "kind": "yes/no",
  "text": "Claim: The star of the 2013 film, \"Coffee, Kill Boss\", had a role in the television series \"IZombie\" which premiered on March 17, 2015.\n\nPassages:\n\n[Coffee, Kill Boss]\nCoffee, Kill Boss is a 2013 film starring Eddie Jemison, Noureen DeWulf and Robert Forster, and co-starring Richard Riehle, Zibby Allen, Chris Wylde, Jack Wallace, Denise Grayson and W. Cameron Tucker.\n\n[Eddie Jemison]\nHe is known for his roles in the \"Ocean's Eleven\" trilogy and the television series \"Hung\" and IZombie.\n\n[IZombie (TV series)]\nThe series premiered on March 17, 2015.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qdbdf78acaa",
  "kind": "yes/no",
  "text": "Claim: Israeli actress, Odeya Rush, is known for her lead role in 2015 American horror comedy film based on the children's book series created in 1984 by R.L. Stine.\n\nPassages:\n\n[Goosebumps (film)]\nGoosebumps is a 2015 American horror comedy film based on the children's book series of the same name by R.L. Stine.\n\n[Odeya Rush]\nOdeya Rush (Hebrew: אודיה רש‎ ‎ ; born Odeya Rushinek; May 12, 1997) is an Israeli actress and model. She is known for her lead roles in \"The Giver\" (2014) and \"Goosebumps\" (2015).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q9b4d2c0345",
  "kind": "yes/no",
  "text": "Tweet: I've said it before and I'll say it again but YOUR MENTAL HEALTH IS SO MUCH MORE IMPORTANT THAN A GOOD GRADE",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qe13588cb1d",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "After many years it is brilliant to laugh at germany",
   "Schadenfreude x"
  ]
 },
 {
  "qid": "q7040e0eb03",
  "kind": "yes/no",
  "text": "Claim: Kristina Ceyton and Rahul Bose produced the debut film of the director, The Nightengale (2017 film).\n\nPassages:\n\n[The Babadook]\nThe Babadook is a 2014 Australian psychological horror film written and directed by Jennifer Kent in her directorial debut, and produced by Kristina Ceyton and Kristian Moliere.\n\n[Jennifer Kent]\nJennifer Kent is an Australian actress, writer and director, best known for her horror film \"The Babadook\" (2014), which was her directorial debut.\n\n[The Nightingale (2017 film)]\nThe Nightingale is an upcoming Australian period thriller film written and directed by Jennifer Kent.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q466e35f7cc",
  "kind": "yes/no",
  "text": "Claim: This person directed the 2006 film that starred Jane Adams (actress). Both he and Zoltan Korda work in the film industry.\n\nPassages:\n\n[Jane Adams (actress)]\nHer film roles include \"Happiness\" (1998), \"Wonder Boys\" (2000), \"Eternal Sunshine of the Spotless Mind\" (2004), and \"Little Children\" (2006).\n\n[Zoltan Korda]\nZoltan Korda (June 3, 1895 – October 13, 1961) was a Hungarian-born motion picture screenwriter, director and producer.\n\n[Little Children (film)]\nLittle Children is a 2006 American drama film directed by Todd Field.\n\n[Todd Field]\nWilliam Todd Field (born February 24, 1964) is an American actor and three-time Academy Award nominated filmmaker.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q3ee6ed1570",
  "kind": "yes/no",
  "text": "Claim: The Woodvale Historic District was built buy a company headquartered in Rockhill Furnace, Pennsylvania.\n\nPassages:\n\n[Woodvale Historic District]\nWoodvale Historic District is a national historic district located at Broad Top Township, Bedford County; Wells Township, Fulton County; and Wood Township, Huntingdon County, Pennsylvania. They were built by the Rockhill Iron and Coal Company.\n\n[East Broad Top Railroad and Coal Company]\nThe East Broad Top Railroad and Coal Company (EBT) is a for-profit, narrow gauge historic railroad headquartered in Rockhill Furnace, Pennsylvania, 19 mi north of Interstate 76 (the Pennsylvania Turnpike) and 11 mi south of U.S. Route 22, the William Penn Highway.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q3b980dc44a",
  "kind": "yes/no",
  "text": "Claim: David Nixon and another man are both directors. The other director directed the film \"Rhinestone\".\n\nPassages:\n\n[Rhinestone (film)]\nRhinestone is a 1984 American musical comedy film directed by Bob Clark from a screenplay by Sylvester Stallone and Phil Alden Robinson and starring Stallone and Dolly Parton.\n\n[David Nixon (director)]\nDavid Nixon is an American film director and film producer.\n\n[Phil Alden Robinson]\nPhil Alden Robinson (born March 1, 1950) is an American film director and screenwriter whose films include \"Field of Dreams\", \"Sneakers\", and \"The Sum of All Fears\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q972ae723c3",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "The only thing I got from college is a caffeine addiction",
   "College is really difficult, expensive, tiring, and I often question if a degree is worth the stress."
  ]
 },
 {
  "qid": "q6dffde5ade",
  "kind": "yes/no",
  "text": "Tweet: love getting assignments at 6:25pm on a Friday!!",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q75973d7280",
  "kind": "yes/no",
  "text": "Claim: The Jiangxia Tidal Power Station is located in a city in Zhejiang Province. That city and the city home to SIAS International University are both in New.\n\nPassages:\n\n[Wenling]\nWenling (Wenling dialect: Uen-lin Zy ] ; ) is a coastal county-level city in the municipal region of Taizhou, in southeastern Zhejiang province, China.\n\n[SIAS International University]\nSias is located in the ancient city of Xinzheng, near Henan's capital, Zhengzhou.\n\n[Xinzheng]\nXinzheng () is a small county-level city of Zhengzhou in the south of Henan province of Central China.\n\n[Jiangxia Tidal Power Station]\nThe Jiangxia Tidal Power Station (江厦潮汐电站) is the fourth largest tidal power station in the world, located in Wuyantou, Wenling City, Zhejiang Province, China.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q946d9659e5",
  "kind": "yes/no",
  "text": "Text: this is the first time in 6 years i haven’t had to move, i am so relieved",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qe33bcb91db",
  "kind": "yes/no",
  "text": "Claim: Five Nights at Freddy's 2, from summer 2002, is the sequel to a game where a player must act as a night security guard, which was a new intellectual property released in 2014.\n\nPassages:\n\n[Five Nights at Freddy's (video game)]\nThe game centers around a fictional pizza restaurant called \"Freddy Fazbear's Pizza\", where the player must act as a night security guard, defending themselves from the malfunctioning, haunted animatronic characters by tracking their movement through the facility using security cameras.\n\n[2014 in video gaming]\nIn addition, it saw the release of many new intellectual properties, such as \"Destiny\", \"Five Nights at Freddy's,\" \"Sunset Overdrive\", \"Titanfall\", \"The Evil Within\" and \"Watch Dogs\".\n\n[Five Nights at Freddy's 2]\nIt is the second game in the \"Five Nights at Freddy's\" series, and is chronologically set before the events of the first game.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q3ad377d4db",
  "kind": "yes/no",
  "text": "Claim: The director of a 2010 British-Canadian supernatural horror film was born on 27 February 1977. A company produced this film. The company co-produced the film Jem and the Holograms.\n\nPassages:\n\n[Insidious (film)]\nInsidious is a 2010 American-Canadian supernatural horror film directed by James Wan, written by Leigh Whannell, and starring Patrick Wilson, Rose Byrne and Barbara Hershey.\n\n[James Wan]\nJames Wan (born 27 February 1977) is a Malaysian-Australian film director, screenwriter, and producer.\n\n[Jem and the Holograms (film)]\nBorrowing elements from the 1980s animated television series \"Jem\" by Christy Marx, the film was produced by Hasbro Studios and Blumhouse Productions.\n\n[Blumhouse Productions]\nBlumhouse is mostly known for producing low-budget horror films, such as \"Paranormal Activity\", \"Insidious\", \"The Purge\", \"Sinister\", \"The Gift\", \"Split\" and \"Get Out\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q7f2febae93",
  "kind": "yes/no",
  "text": "Claim: Alfred Döblin and César Vallejo were not both German nationals.\n\nPassages:\n\n[César Vallejo]\nCésar Abraham Vallejo Mendoza (March 16, 1892 – April 15, 1938) was a Peruvian poet, writer, playwright, and journalist.\n\n[Alfred Döblin]\nBruno Alfred Döblin (10 August 1878 – 26 June 1957) was a German novelist, essayist, and doctor, best known for his novel \"Berlin Alexanderplatz\" (1929).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qca1d387748",
  "kind": "yes/no",
  "text": "Claim: The Wild came years before this film. The film starred Lake Bell.\n\nPassages:\n\n[Lake Bell]\nShe has starred in various television series, including \"Boston Legal\" (2004–2006), \"Surface\" (2005–2006), \"How to Make It in America\" (2010–2011) and \"Childrens Hospital\" (2008–2016), and in films including \"Over Her Dead Body\" (2008), \"What Happens in Vegas\" (2008), \"It's Complicated\" (2009), \"No Strings Attached\" (2011), \"Million Dollar Arm\" (2014) and \"The Secret Life of Pets\" (2016).\n\n[Million Dollar Arm]\nMillion Dollar Arm is a 2014 American biographical sports drama film directed by Craig Gillespie and produced by Walt Disney Pictures from a screenplay written by Thomas McCarthy.\n\n[The Wild]\nThe Wild is a 2006 American 3D computer animated comedy directed by animator Steve \"Spaz\" Williams, and written by Ed Decter, John J. Strauss, Mark Gibson and Philip Halprin.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q75103eb8e0",
  "kind": "yes/no",
  "text": "Claim: Bridge of Spies stars a Soviet intelligence agent with the name Rudolf Abel.\n\nPassages:\n\n[Rudolf Abel]\nRudolf Ivanovich Abel (Russian: Рудольф Иванович Абель ), real name Vilyam \"Willie\" Genrikhovich Fisher (Вильям \"Вилли\" Генрихович Фишер), (July 11, 1903 – November 15, 1971) was a Soviet intelligence officer.\n\n[Bridge of Spies (film)]\nSet during the Cold War, the film tells the story of lawyer James B. Donovan, who is entrusted with negotiating the release of Francis Gary Powers—a U.S. Air Force pilot whose U-2 spy plane was shot down over the Soviet Union in 1960—in exchange for Rudolf Abel, a convicted Soviet KGB spy held under the custody of the United States, whom he represented at trial.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qe7f6de332c",
  "kind": "yes/no",
  "text": "Text: You know what makes a 15 minute wait for the bus even better, rum leaking all over the contents of your bag 🙈😫",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qcb5a3f0f1c",
  "kind": "yes/no",
  "text": "Claim: The Magic Roundabout is a 2005 French-British, computer-animated, adventure fantasy film based on the comedic television series The Magic Roundabout.\n\nPassages:\n\n[Ray Winstone]\nHe has also become well known as a voice over actor, and has recently branched out into film production.\n\n[The Magic Roundabout (film)]\nThe Magic Roundabout (released in France as Pollux - Le manège enchanté and redubbed in the United States as Doogal or The Lord of the Springs) is a 2005 French-British computer-animated adventure fantasy film based on the television series \"The Magic Roundabout\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q47623faea6",
  "kind": "yes/no",
  "text": "Claim: The King of Hungary and Chicago who transferred Schottenkirche to German-speaking Benedictine monks was born on 10 August 139727.\n\nPassages:\n\n[Schottenkirche, Vienna]\nIn 1418, the Duke Albert V of Austria transferred it to the German-speaking Benedictine monks from the Melk Abbey during the Melker Reform initiated after the Council of Constance.\n\n[Albert II of Germany]\nAlbert the Magnanimous KG (10 August 139727 October 1439) was King of Hungary and Croatia from 1437 until his death.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qeb714de1ff",
  "kind": "yes/no",
  "text": "Claim: \"I Do\" the song by Filipino singer Nina and described to be Mariah Carey-like was on third studio album, \"Nina\".\n\nPassages:\n\n[Mariah Carey]\nMariah Carey (born March 27, 1969 or 1970) is an American singer, songwriter, record producer, and actress.\n\n[I Do (Nina Girado song)]\n\"I Do\" is a song by Filipino singer Nina from her self-titled third studio album, \"Nina\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q1c2a1fe63b",
  "kind": "yes/no",
  "text": "Claim: K-Pax Racing participates in a drag racing series. The organization that has sanctioned this series since 2017 has sanctioned races in both California and Indianapolis.\n\nPassages:\n\n[Pirelli World Challenge]\nIt is managed by WC Vision since 2008, and is sanctioned by the United States Auto Club since 2017.\n\n[1991 USAC FF2000 Championship]\nThe series was sanctioned by the United States Auto Club and ran races in California and Arizona.\n\n[K-Pax Racing]\nK-PAX Racing is an automobile racing team in the SCCA's Pirelli World Challenge racing series.\n\n[United States Auto Club]\nFrom 1956 to 1979, USAC sanctioned the United States National Championship, and from 1956 to 1997 the organization sanctioned the Indianapolis 500.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q08895806ee",
  "kind": "yes/no",
  "text": "Claim: Julia Compton Moore was the wife of the United States Army lieutenant general who received the Distinguished Service Cross, and was the first of his West Point class to be promoted to brigadier general, major general, and lieutenant general.\n\nPassages:\n\n[Julia Compton Moore]\nJulia Compton Moore (February 10, 1929April 18, 2004) was the wife of Lieutenant General (Ret.) Hal Moore, a United States Army officer.\n\n[Hal Moore]\nHarold Gregory \"Hal\" Moore, Jr. (February 13, 1922 – February 10, 2017) was a United States Army lieutenant general and author. He was a recipient of the Distinguished Service Cross, which is the U.S. military's second highest decoration for valor, and was the first of his West Point class (1945) to be promoted to brigadier general, major general, and lieutenant general.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q00a5e68f07",
  "kind": "yes/no",
  "text": "Claim: The business in an Mexican state, lasting from 1873 to 1883, became one of the most noted mercury producers in the world. Eastlake in a county in the Mexican state is located southwest of it. Eriogonum nervulosum is a plant found in this county.\n\nPassages:\n\n[Eastlake, Lake County, California]\nIt was located just southwest of the Sulphur Bank Mine 7 mi north-northwest of Lower Lake, at an elevation of 1355 feet (413 m).\n\n[Sulphur Bank Mine]\nThe 150 acre mine became one of the most noted mercury producers in the world.\n\n[Eriogonum nervulosum]\nThis uncommon plant is endemic to the inland North Coast Ranges of California, where it is known from only a handful of occurrences, most of which are in Lake County.\n\n[Lower Lake Stone Jail]\nDuring the days of the first quicksilver operations of the Sulphur Bank Mine, lasting from 1873 to 1883, rapid town growth and the urgent need for civil order necessitated the building of a jail.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 }
]
