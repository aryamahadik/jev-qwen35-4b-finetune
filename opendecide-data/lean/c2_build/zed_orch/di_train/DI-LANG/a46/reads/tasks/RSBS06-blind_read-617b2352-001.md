# A46 replay label-noise blind read RSBS06-blind_read-617b2352-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS06-blind_read-617b2352-001.json

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
  "qid": "q4152782a1e",
  "kind": "yes/no",
  "text": "Claim: Kenneth \"Ken\" Leung is the actor that portrays a marvel character in a ABC television series that was created by Scott Buck in 1962.\n\nPassages:\n\n[Inhumans (TV series)]\nMarvel's Inhumans, or simply Inhumans, is an American television series created for ABC by Scott Buck, based on the Marvel Comics race of the same name.\n\n[Ken Leung]\nKenneth \"Ken\" Leung (born January 21, 1970) is an American actor who is best known for playing Miles Straume in \"Lost\", Admiral Statura in \"\", Detective Stephen Sing in \"Saw\", and Kid Omega in \"\". He portrays the Marvel Comics character Karnak, a member of the Inhumans, on the ABC television series \"Inhumans\", which premiered in September 2017.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q8ff5b1bd45",
  "kind": "yes/no",
  "text": "Claim: The town Shelley Watts was born in is a larger town than Bonny Hills. Cyneoterpna wilsoni is found in this town.\n\nPassages:\n\n[Bonny Hills, New South Wales]\nBonny Hills is a town in New South Wales, Australia about 30 minutes drive south of Port Macquarie. As of the 2011 census, it had a population of 2,870 people.\n\n[Shelley Watts]\nShelley Watts (born 10 August 1987 in Port Macquarie) is an amateur boxer from Australia.\n\n[Cyneoterpna wilsoni]\nIt is found in Queensland, New South Wales, Victoria, South Australia and Tasmania.\n\n[Port Macquarie]\nPort Macquarie is a coastal town in the local government area of Port Macquarie-Hastings. The town with its suburbs had a population of 45,698 in June 2016.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q92115186f4",
  "kind": "yes/no",
  "text": "Claim: The T-Type is a series of Buick logos that were popular during the 1980s, this marketing approach for Buick products was a revival of a similar approach used in the 1960s (and later revived in the 1990s) with the Buick GS designation used on several high-volume cars built by Buick since 1965.\n\nPassages:\n\n[T-Type]\nThis marketing approach for Buick products was a revival of a similar approach used in the 1960s (and later revived in the 1990s) with the Buick GS designation.\n\n[Buick Gran Sport]\nThe Gran Sport name has been used on several high-performance cars built by Buick since 1965.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qce51bbc099",
  "kind": "yes/no",
  "text": "Claim: \"Angry Dad: The Movie\" is the fourteenth episode of a simpson's season that did not begin airing on September 26, 2010.\n\nPassages:\n\n[Angry Dad: The Movie]\n\"Angry Dad: The Movie\" is the fourteenth episode of \"The Simpsons\"<nowiki>'</nowiki> twenty-second season.\n\n[The Simpsons (season 22)]\n\"The Simpsons\"' twenty-second season began airing on Fox on September 26, 2010 and ended on May 22, 2011.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q522aa4d5e9",
  "kind": "yes/no",
  "text": "Claim: The man in Mad Men who had Peggy Olson as a secretary, played a role in the comedy series \"30 Rock\" as well as the drama series \"Mad Men\".\n\nPassages:\n\n[Peggy Olson]\nInitially, Peggy is secretary to Don Draper (Jon Hamm), creative director of the advertising agency Sterling Cooper.\n\n[Jon Hamm]\nJonathan Daniel Hamm (born March 10, 1971) is an American actor, director, and television producer best known for playing advertising executive Don Draper for the AMC television drama series, \"Mad Men\" (2007–2015).\n\n[Live Show]\n\"Live Show\" featured appearances by Rachel Dratch, Bill Hader, Matt Damon, Jon Hamm, and Julia Louis-Dreyfus.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qa88e872728",
  "kind": "yes/no",
  "text": "Claim: Brutti di notte is a parody of the film starring French actress, Catherine Deneuve.\n\nPassages:\n\n[Belle de Jour (film)]\nBelle de Jour (] ) is a 1967 French drama film directed by Luis Buñuel and starring Catherine Deneuve, Jean Sorel, and Michel Piccoli.\n\n[Brutti di notte]\nIt is a parody of Luis Buñuel's film \"Belle de Jour\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qb8625e8d72",
  "kind": "yes/no",
  "text": "Claim: Harold Robert Isaacs joined the department of political science of a University in 1953. The institute where Leigh Tesfatsion received her doctorate is located in more cities than the University that Harold Isaacs joined.\n\nPassages:\n\n[University of Minnesota]\nThe University of Minnesota, Twin Cities (often referred to as The University of Minnesota, Minnesota, the U of M, UMN, or simply the U) is a public research university in Minneapolis and Saint Paul, Minnesota.\n\n[Harold Isaacs]\nIn 1953 he joined the department of political science at the Massachusetts Institute of Technology.\n\n[Leigh Tesfatsion]\nShe received her doctorate at the University of Minnesota, and taught at the University of Southern California before moving to Iowa State.\n\n[Massachusetts Institute of Technology]\nThe Massachusetts Institute of Technology (MIT) is a private research university in Cambridge, Massachusetts.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q473b8b5b24",
  "kind": "yes/no",
  "text": "Claim: The Colbert Report is a satirical Comedy Central program. The director of Splatter Theatre directed the host of The Colbert Report.\n\nPassages:\n\n[Stephen Colbert]\nHe is best known for hosting the satirical Comedy Central program \"The Colbert Report\" from 2005 to 2014, and hosting the CBS talk program \"The Late Show with Stephen Colbert\" beginning in September 2015.\n\n[Splatter Theatre]\nThe show was first performed at the Cabaret Metro, on October 31, 1987 and directed by Mick Napier.\n\n[Mick Napier]\nHe has directed Stephen Colbert, Tina Fey, Rachel Dratch, Horatio Sanz, Nia Vardalos, Andy Richter, Jeff Garlin, and David Sedaris, amongst others.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q76b10b063c",
  "kind": "yes/no",
  "text": "Claim: The founder of the Westboro Baptist Church died in 2014.\n\nPassages:\n\n[The Most Hated Family in America]\nThe Most Hated Family in America is a 2007 BBC documentary film written and presented by Louis Theroux about the family at the core of the Westboro Baptist Church. The organization was led by Fred Phelps (who has since died) and located in Topeka, Kansas.\n\n[Fred Phelps]\nFred Waldron Phelps Sr. (November 13, 1929 – March 19, 2014) was an American Baptist minister and civil rights attorney who became notorious for his vehement anti-homosexual rhetoric and protests near the funerals of homosexuals, military veterans, and disaster victims, whose deaths, he believed, were the result of God’s hatred of America’s \"bankrupt values\" and tolerance of homosexual lifestyles.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q405eb22c74",
  "kind": "yes/no",
  "text": "Claim: Munich beat the Tajikistan in a sporting event. Jack Taylor (referee) was famous for officiating at this event.\n\nPassages:\n\n[Jack Taylor (referee)]\nJohn Keith \"Jack\" Taylor, OBE (21 April 1930 – 27 July 2012) was an English football referee, famous for officiating in the 1974 FIFA World Cup Final during which he awarded two penalties in the first 30 minutes.\n\n[1974 FIFA World Cup Final]\nThe 1974 FIFA World Cup Final was the final match of the 1974 FIFA World Cup, the 10th FIFA World Cup, a competition to determine the world champion among national men's football sides. The match was contested by the Netherlands and West Germany, with the West Germans winning 2–1.\n\n[Football in Munich]\nMunich is one of the most successful footballing cities in Europe and the World with over 40 trophies, including Germany's victory in the 1974 FIFA World Cup Final.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2cad5319cb",
  "kind": "yes/no",
  "text": "Claim: The year of the event which occurred first out of when Beecher's Handmade Cheese was founded, and when Pike Place Market opened is 1907.\n\nPassages:\n\n[Pike Place Market]\nPike Place Market is a public market overlooking the Elliott Bay waterfront in Seattle, Washington, United States. The Market opened August 17, 1907, and is one of the oldest continuously operated public farmers' markets in the United States.\n\n[Beecher's Handmade Cheese]\nBeecher's Handmade Cheese is an artisan cheesemaker and retail shop with locations in the Pike Place Market, Seattle, Washington and New York City's Flatiron District. The company was founded by Kurt Beecher Dammeier in 2003 and opened in the Pike Place Market after Dammeier obtained a difficult to obtain storefront lease in the Market.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q06fa90fe0a",
  "kind": "yes/no",
  "text": "Claim: Both Orson Scott Card's novel \"Ender's Game\" and \"The Bone People,\"by the author whose work inspired the film \"Hooks and Feelers\" starring Bridgette Allen, both came out in 1985.\n\nPassages:\n\n[Bridgette Allen]\nShe also starred in the film \"Hooks and Feelers\", which was an adaptation of a Keri Hulme story.\n\n[Orson Scott Card]\nHis novel \"Ender's Game\" (1985) and its sequel \"Speaker for the Dead\" (1986) both won Hugo and Nebula Awards, making Card the only author to win both science fiction's top U.S. prizes in consecutive years.\n\n[Keri Hulme]\nHer only novel, \"The Bone People\", won the Booker Prize in 1985.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qadcea0ecc3",
  "kind": "yes/no",
  "text": "Claim: J. Walter Duncan sold the USFL team who played home baseball games at Giants Stadium to Donald Trump in 1983.\n\nPassages:\n\n[New Jersey Generals]\nHome games were played at Giants Stadium in East Rutherford, New Jersey, which was called The Meadowlands for Generals games.\n\n[J. Walter Duncan]\nIn 1983, he became owner of the New Jersey Generals, he sold the team to Donald Trump after the 1983 USFL season.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q895cf2ef97",
  "kind": "yes/no",
  "text": "Claim: The band Len Tuckey was a guitarist for, released a version of a song. The song was released a few days earlier than the artist born as Geoffrey Beck.\n\nPassages:\n\n[Len Tuckey]\nIn a career spanning more than 40 years, Tuckey was the guitarist for the Attack and the Nashville Teens, and came to prominence in the early 1970s as the lead guitarist for Suzi Quatro.\n\n[The Attack (band)]\nThe Attack were a freakbeat/psychedelic rock band formed in 1966 around singer Richard Shirman (born 26 April 1949, London Died July 2017) The first line-up featured drummer Alan Whitehead from Marmalade, guitarist David O'List (later of The Nice) and John Du Cann (later of Andromeda and Atomic Rooster). They also released a version of \"Hi Ho Silver Lining\", a few days earlier than Jeff Beck.\n\n[Jeff Beck]\nGeoffrey Arnold \"Jeff\" Beck (born 24 June 1944) is an English rock guitarist.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q8411d7a3d0",
  "kind": "yes/no",
  "text": "Claim: The boxer that defeated Oliver Lavigilante in the 2012 Summer Olympics is of Russian nationality.\n\nPassages:\n\n[Oliver Lavigilante]\nJason Oliver Lavigilante is a Mauritian boxer. At the 2012 Summer Olympics, he competed in the Men's flyweight, but was defeated in the first round by Duke Micah.\n\n[Duke Micah]\nDuke Akueteh Micah (born 16 September 1991) is a Ghanaian boxer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3c9646646b",
  "kind": "yes/no",
  "text": "Claim: Celebrity Fifteen to One has had more than one appearance by an English writer and former Conservative Member of Parliament.\n\nPassages:\n\n[Celebrity Fifteen to One]\nCelebrity Fifteen to One is a celebrity version of the Channel 4 game show \"Fifteen to One\". Richard Whiteley, Anna Raeburn, Sally Jones and Rory McGrath appeared on both 1990s episodes, with Alex Brooker, Jimmy Carr, Johnny Vegas, Rhod Gilbert and Gyles Brandreth also having made appearances on more than one episode.\n\n[Gyles Brandreth]\nGyles Daubeney Brandreth (born 8 March 1948) is an English writer, broadcaster, actor, and former Conservative Member of Parliament.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q2ec96cd241",
  "kind": "yes/no",
  "text": "Claim: The Emerald Wand of Oz was published by the comapny that is headquartered in New York City.\n\nPassages:\n\n[The Emerald Wand of Oz]\nThe book is illustrated by William Stout and published by Harper Collins.\n\n[HarperCollins]\nThe company is headquartered in New York City and is a subsidiary of News Corp.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q0273f1ebb6",
  "kind": "yes/no",
  "text": "Claim: The American basketball coach which Boston Celtics hired in 2004–05 was born on October 13, 1961.\n\nPassages:\n\n[2004–05 Boston Celtics season]\nThe season is memorable when the team hired Doc Rivers to be their head coach for the upcoming season.\n\n[Doc Rivers]\nGlenn Anton \"Doc\" Rivers (born October 13, 1961) is an American basketball coach and former player.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf21b31bad0",
  "kind": "yes/no",
  "text": "Claim: The Irish folk band \"The Wolfe Tones,\" known for their album Sing Out for Ireland, are named after Theobald Wolfe Tone, the Irish statesman and patriot.\n\nPassages:\n\n[The Wolfe Tones]\nThey take their name from the Irish rebel and patriot Theobald Wolfe Tone, one of the leaders of the Irish Rebellion of 1798, with the \"double entendre\" of a wolf tone – a spurious sound that can affect instruments of the violin family.\n\n[Sing Out for Ireland]\nSing Out for Ireland is the fourteenth album by Irish folk and rebel band The Wolfe Tones.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qa6ddaf19a4",
  "kind": "yes/no",
  "text": "Claim: Jayantabhai Ki Luv Story includes a lead role for the film actress and model who is a native of Bihar.\n\nPassages:\n\n[Neha Sharma]\nNeha Sharma (] ; born 21 November 1987) is an Indian film actress and model. A native of Bihar, Sharma attended the Mount Carmel School in Bhagalpur and pursued a course in fashion design from the National Institute of Fashion Technology (NIFT) in New Delhi.\n\n[Jayantabhai Ki Luv Story]\nThe film stars Vivek Oberoi opposite Neha Sharma in lead roles.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qfdcb5a263f",
  "kind": "yes/no",
  "text": "Claim: The awards ceremony that was hosted in 2007 by an American commercial broadcast television network headquartered on Pico Boulevard was hosted at the Shrine Auditorium in Texas.\n\nPassages:\n\n[Fox Broadcasting Company]\nFox Broadcasting Company (often shortened to Fox and stylized as FOX) is an American commercial broadcast television network owned by Fox Entertainment Group, a subsidiary of 21st Century Fox. The network is headquartered at 20th Century Fox studio on Pico Boulevard in Century City of Los Angeles with additional major offices and production facilities at the Fox Television Center in nearby West Los Angeles and Fox Broadcasting Center in the Yorkville neighborhood of Manhattan, New York City.\n\n[59th Primetime Emmy Awards]\nThe 59th Primetime Emmy Awards were held on Sunday, September 16, 2007, honoring the best in U.S. prime time television programming at the Shrine Auditorium in Los Angeles, California. The ceremony was televised live on Fox at 8:00 p.m. EDT for the first time in high definition (on tape delay three hours later on the West Coast of the United States at 8:00 p.m.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q29adcdbe81",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "love how badly i embarrass myself on nights out how iconic X",
   "I hate that I always embarrass myself on nights out, how shameful."
  ]
 },
 {
  "qid": "q194a389522",
  "kind": "yes/no",
  "text": "Claim: Charlton Heston starred in the film The Human Factor in 1979, alongside fellow English actors Richard Attenborough and Derek Jacobi.\n\nPassages:\n\n[The Human Factor (1979 film)]\nThe Human Factor is a 1979 British thriller film starring Richard Attenborough, Nicol Williamson, Derek Jacobi, and John Gielgud.\n\n[Derek Jacobi]\nSir Derek George Jacobi, ( ; born 22 October 1938) is an English actor and stage director.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q5aa850175b",
  "kind": "yes/no",
  "text": "Claim: Joseph Mansfield Santley was born first. The director of A Better Tomorrow was born after him.\n\nPassages:\n\n[John Woo]\nJohn Woo SBS (Ng Yu-Sum; born 1 May 1946) is a Chinese-born Hong Kong film director, writer, and producer.\n\n[A Better Tomorrow]\nA Better Tomorrow () is a 1986 Hong Kong crime film directed by John Woo and starring Ti Lung, Leslie Cheung and Chow Yun-fat.\n\n[Joseph Santley]\nJoseph Mansfield Santley (born Joseph Ishmael Mansfield, January 10, 1890 – August 8, 1971) was an American actor, singer, dancer, writer, director, and producer of musical theatrical plays motion pictures and television shows.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q5a11f4269c",
  "kind": "yes/no",
  "text": "Claim: The chain that Jack O'Shea's was formerly located in, in London is the UK's second largest shop, Harrods - today owned by the State of Qatar - is the biggest.\n\nPassages:\n\n[Selfridges]\nThe flagship store on London's Oxford Street is the second largest shop in the UK (after Harrods) and opened 15 March 1909.\n\n[Jack O'Shea's]\nThe chain was formerly located in Selfridges, but had its contract terminated in 2012 after breaking the store's ethical code on selling foie gras.\n\n[Harrods]\nIt is owned by the state of Qatar.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q9d829be5a4",
  "kind": "yes/no",
  "text": "Text: Can anybody explain why all hotel shampoo smells like the taste of grape flavored medicine?",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q0f59dd37d1",
  "kind": "yes/no",
  "text": "Post: i haven’t thought about the mysterious benedict society in years omg",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qee38454f3b",
  "kind": "yes/no",
  "text": "Claim: George V, who died in 1936, was the Spanish king to whom Rev James MacGregor was made chaplain.\n\nPassages:\n\n[George V]\nGeorge V (George Frederick Ernest Albert; 3 June 1865 – 20 January 1936) was King of the United Kingdom and the British Dominions, and Emperor of India, from 6 May 1910 until his death in 1936.\n\n[James MacGregor (moderator)]\nVery Rev James MacGregor DD FRSE (1832-1910) Scottish minister and philanthropist. He was Moderator of the General Assembly of the Church of Scotland in 1891. In 1886 he was made Chaplain in Ordinary to Queen Victoria, in 1901 Chaplain to King Edward VII, and in 1910 to King George V, serving three monarchs in all.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q2101bd05a1",
  "kind": "yes/no",
  "text": "Claim: The name of Norman Jewison character in the film, where Bostin Christopher had a small role, is David Dunn.\n\nPassages:\n\n[Unbreakable (film)]\nIn \"Unbreakable\", a security guard named David Dunn survives a horrific train crash.\n\n[Bostin Christopher]\nChristopher also had a small role in M. Night Shyamalan's \"Unbreakable\", as a Comic Book Clerk.\n\n[David Dunn (character)]\nDavid Dunn is a fictional character and the main protagonist in the \"Unbreakable\" film series, portrayed by American actor Bruce Willis.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qf2e63ad941",
  "kind": "yes/no",
  "text": "Claim: The Dutch man who along with Rexach was acquired in the 1993–94 Inter Milan season, manages Cruyff Football together with the footballer who is also currently manager of Tel Aviv team.\n\nPassages:\n\n[Jordi Cruyff]\nJohan Jordi Cruijff (] , anglicised to Cruyff; born 9 February 1974) is a Dutch former footballer. Cruyff is currently Maccabi Tel Aviv's manager.\n\n[Wim Jonk]\nTogether with Jordi Cruyff, Jonk manages Cruyff Football and is responsible for the worldwide continuation and dissemination of the football legacy of Dutch football legend Johan Cruyff, who died on March 24, 2016.\n\n[1993–94 Inter Milan season]\nIn the summer of 1993, Inter acquired Dutch men Dennis Bergkamp and Wim Jonk, already spotted in the previous winter.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q27a4654c78",
  "kind": "yes/no",
  "text": "Text: Football is turning into an anatomy lesson. COOL",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q62fa168379",
  "kind": "yes/no",
  "text": "Claim: A pair of terraces on the Carlton House Terrace street took the place of this house. George IV was the Prince Regent likely to have stayed in that house in 1811.\n\nPassages:\n\n[George IV of the United Kingdom]\nGeorge IV (George Augustus Frederick; 12 August 1762 – 26 June 1830) was King of the United Kingdom of Great Britain and Ireland and of Hanover following the death of his father, George III, on 29 January 1820, until his own death ten years later. From 1811 until his accession, he served as Prince Regent during his father's final mental illness.\n\n[Carlton House]\nCarlton House was a mansion in London, best known as the town residence of the Prince Regent for several decades from 1783.\n\n[Carlton House Terrace]\nThey took the place of Carlton House, and the freehold still belongs to the Crown Estate.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qdd32998c62",
  "kind": "yes/no",
  "text": "Claim: Pam Shriver and the player Loic Courteau coached were both alive in the 1960s.\n\nPassages:\n\n[Loïc Courteau]\nCourteau has coached the French Fed Cup team in years past, and has been the coach of Amélie Mauresmo, the winner of two Grand Slams, since 2002.\n\n[Pam Shriver]\nPamela Howard Shriver (born July 4, 1962) is an American former professional tennis player known primarily as a doubles specialist with success also as a singles player.\n\n[Amélie Mauresmo]\nAmélie Simone Mauresmo ] (born 5 July 1979) is a French former professional tennis player, and a former world No. 1.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qdde3189a34",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "I'd like to thank middle aged men watching the Olympics for solving the mental health crisis. Getting someone to shout \"get some perspective\" at every athlete struggling with anxiety will definitely solve their problem.",
   "It's annoying that middle aged men are declaring people with mental health issues need to find some perspective; that's insensitive and unhelpful."
  ]
 },
 {
  "qid": "qea080adb8c",
  "kind": "yes/no",
  "text": "Claim: The former Oklahoma City mayor that features alongside Kevin Ogle on Flashpoint, is younger than Tom Coburn.\n\nPassages:\n\n[Tom Coburn]\nThomas Allen \"Tom\" Coburn (born March 14, 1948) is an American politician and medical doctor.\n\n[Kevin Ogle]\nOgle also serves as moderator of the locally-produced Sunday morning political affairs talk show \"Flashpoint\", alongside panelists Mike Turpen and former Oklahoma City mayor Kirk Humphreys.\n\n[Kirk Humphreys]\nKirk Humphreys (born September 13, 1950) is an American politician who served as Mayor of Oklahoma City from April 9, 1998 to November 3, 2003.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q9422072b08",
  "kind": "yes/no",
  "text": "Tweet: @DylanPetit17 @jaredj5 Let's listen to Dylan Petit over actually doctors, biologists and epidemiologists. 🙄",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qcba95bcdb7",
  "kind": "yes/no",
  "text": "Claim: This series developer created T-Dog on the Walking Dead. He is the American-born US film director renowned for adapting a writer's novellas to the screen, including The Mist and The Green Mile. The writer wrote the novel on which the miniseries The Tommyknockers is based.\n\nPassages:\n\n[T-Dog (The Walking Dead)]\n\"He was created by series developer Frank Darabont and portrayed by IronE Singleton.\n\n[Frank Darabont]\nAs a director he is known for his film adaptations of Stephen King novellas and novels such as \"The Shawshank Redemption\", \"The Green Mile\", and \"The Mist\".\n\n[The Mist (film)]\nThe film was written and directed by Frank Darabont.\n\n[The Tommyknockers (miniseries)]\nThe Tommyknockers is a 1993 television miniseries based on the novel of the same name by Stephen King.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qd54d949eac",
  "kind": "yes/no",
  "text": "Claim: The faster roller coaster, between the ride next to Tidal Wave and Green Lantern has a top speed of 65 mph.\n\nPassages:\n\n[The Riddler's Revenge]\nIt stands 156 ft tall and features a top speed of 65 mph .\n\n[Tidal Wave (Six Flags Magic Mountain)]\nThe entrance to the ride is next to The Riddler's Revenge which is near to JB's Smokehouse BBQ.\n\n[Green Lantern (Six Flags Great Adventure)]\n\"Green Lantern\" stands 155 ft tall and features a top speed of 63 mph .",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q78258a9841",
  "kind": "yes/no",
  "text": "Claim: The song, which features alongside Overture (The Who Song) on the band's fourth studio album of the same name, reached the top 10 on the UK charts and No. 19 on the U.S. \"Billboard\" Hot 100.\n\nPassages:\n\n[Tommy (album)]\nTommy is the fourth studio album by the English rock band The Who, a double album first released in May 1969.\n\n[Pinball Wizard]\nThe original recording was released as a single in 1969 and reached No. 4 in the UK charts and No. 19 on the U.S. \"Billboard\" Hot 100.\n\n[Overture (The Who song)]\nThe track is one of three instrumental tracks released on \"Tommy\", although it does feature some lyrics towards the end; the other two being \"Underture\" and \"Sparks\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q6c609eb9f9",
  "kind": "yes/no",
  "text": "Claim: Robert Bozic fought and lost to a professional boxer with the nickname, Easton Assassin.\n\nPassages:\n\n[Larry Holmes]\nLarry Holmes (born November 3, 1949) is an American former professional boxer who competed from 1973 to 2002. He grew up in Easton, Pennsylvania, which gave birth to his boxing nickname of the \"Easton Assassin\".\n\n[Bob Bozic]\nRobert Bozic (born 1950) was a professional heavyweight boxer from Toronto, Canada between 1970-77. He fought and lost to Larry Holmes in Madison Square Garden in 1973.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q1274ad630d",
  "kind": "yes/no",
  "text": "Claim: The primary duty of the Austrian Pinscher and the Maremma Sheepdog is to guard.\n\nPassages:\n\n[Maremma Sheepdog]\nThe Maremma Sheepdog, in Italian Cane da pastore Maremmano-Abruzzese, is a breed of livestock guardian dog indigenous to central Italy, particularly to Abruzzo and the Maremma region of Tuscany and Lazio. It has been used for centuries by Italian shepherds to guard sheep from wolves.\n\n[Austrian Pinscher]\nThe Austrian Pinscher (Österreichischer Pinscher, FCI No. 64) is a medium-sized breed of pinscher-type dog from Austria, where dogs of the type were originally farm dogs, keeping barns free of rats and acting as home guards, livestock guardians, and drovers.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q72778e844e",
  "kind": "yes/no",
  "text": "Claim: This director is known for his work on blockbuster hit Miss Potter. The Academy of Motion Picture Arts and Sciences presents the award in which he was nominated for his work in the movie that Neal Scanlan worked on.\n\nPassages:\n\n[Miss Potter]\nMiss Potter is a 2006 Anglo-American biographical fiction family drama film directed by Chris Noonan.\n\n[Chris Noonan]\nChris Noonan (born 14 November 1952) is a Sydney-based Australian filmmaker and actor best known for the family film \"Babe\" (1995), for which he was nominated for both the Academy Award for Best Director and Academy Award for Best Adapted Screenplay.\n\n[Neal Scanlan]\nHe worked as both on \"\", and won an Academy Award for Best Visual Effects for the film \"Babe\" in 1996.\n\n[Academy Award for Best Director]\nThe Academy Award for Best Director (officially known as the Academy Award for Best Directing) is an award presented annually by the Academy of Motion Picture Arts and Sciences (AMPAS).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qc88d1d1447",
  "kind": "yes/no",
  "text": "Text: roll n' square sausage and a cup of tea from Robyn's Nest on Maryhill Rd. AMAZING.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q518b7db31c",
  "kind": "yes/no",
  "text": "Claim: Scott Workman was an American stuntman and actor credited with a successful show on the smaller TV network WB Television Network.\n\nPassages:\n\n[Buffy the Vampire Slayer]\nAlthough such ratings are lower than successful shows on the \"big four\" networks (ABC, CBS, NBC, and Fox), they were a success for the relatively new and smaller WB Television Network.\n\n[Scott Workman]\nWilliam Scott Workman (September 16, 1966 - September 29, 2013) was an American stuntman and actor whose career spanned over the course of 20 years. Television credits include \"The X-Files\", \"Buffy the Vampire Slayer\" and \"Sons of Anarchy\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6ee2048a66",
  "kind": "yes/no",
  "text": "Claim: WWF The Music, Vol. 5 is a soundtrack album whose songs were composed and performed by an American music composer best known for his work with WWE (formerly WWF) from March 1985 onward.\n\nPassages:\n\n[WWF The Music, Vol. 5]\nWWF The Music, Vol. 5 is a soundtrack album by WWE (then known as the World Wrestling Federation, or WWF). Released on February 20, 2001 by Koch Records, it features entrance theme music of various WWE superstars, all of which were composed and performed by Jim Johnston (with the exception of one song, performed by Motörhead).\n\n[Jim Johnston (composer)]\nJames Alan \"Jim\" Johnston (born 1959) is an American music composer best known for his work with WWE (formerly WWF) from 1985 onwards.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qbf1f963d82",
  "kind": "yes/no",
  "text": "Claim: Peter Rufai was the goalkeeper that participated in a football game for a movie premiere. The movie was the first movie aggregated on the CREETIQ website.\n\nPassages:\n\n[A Trip to Jamaica]\nA Trip to Jamaica is a Nigerian comedy drama film directed by Robert Peters, starring Ayo Makun, Funke Akindele, Nse Ikpe Etim and Dan Davies. The event also featured a celebrity football game involving ex-internationals, like Kanu Nwankwo, Jay Jay Okocha, Peter Rufai, Joseph Yobo and Stephen Appiah.\n\n[Peter Rufai]\nPeter Rufai (born 24 August 1963) is a Nigerian retired footballer who played as a goalkeeper.\n\n[CREETIQ]\nThe first movie aggregated on the website was Ayo Makun's A Trip to Jamaica.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q47b091e878",
  "kind": "yes/no",
  "text": "Claim: The American retired professional basketball player born on July 30, 1963 was re-signed to Warriors during the offseason of 2000–01 NBA on a two year contract.\n\nPassages:\n\n[Chris Mullin (basketball)]\nChristopher Paul Mullin (born July 30, 1963) is an American retired professional basketball player and current head coach of the St. John's Red Storm.\n\n[2000–01 Golden State Warriors season]\nThe 2000–01 NBA season was the Warriors' 55th season in the National Basketball Association, and 39th in the San Francisco Bay Area. During the offseason, the Warriors re-signed free agent and former All-Star forward Chris Mullin, while acquiring Danny Fortson from the Boston Celtics and Bob Sura from the Cleveland Cavaliers.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qfb9d81d7e5",
  "kind": "yes/no",
  "text": "Claim: A British author wrote the books the 2000 TV series The Jewel in the Crown were based on. Both he and the writer of Amédée, or How to Get Rid of It, are playwrights that lived during the same time period.\n\nPassages:\n\n[Eugène Ionesco]\nEugène Ionesco (born Eugen Ionescu, ] ; 26 November 1909 – 28 March 1994) was a Romanian-French playwright who wrote mostly in French, and one of the foremost figures of the French Avant-garde theatre.\n\n[Paul Scott (novelist)]\nPaul Mark Scott (25 March 19201 March 1978) was an English novelist, playwright, and poet, best known for his monumental tetralogy \"The Raj Quartet.\"\n\n[Amédée, or How to Get Rid of It]\nAmédée, or How to Get Rid of It (French: \"Amédée ou comment s'en débarrasser\" ) is a play written by Eugène Ionesco in 1954 based on his earlier short story entitled \"Oriflamme\".\n\n[The Jewel in the Crown (TV series)]\nThe Jewel in the Crown is a 1984 British television serial about the final days of the British Raj in India during and after World War II, based upon the \"Raj Quartet\" novels (1965–75) by British author Paul Scott.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q23af6e7e42",
  "kind": "yes/no",
  "text": "Text: i heard marvins room again so naturally i just went ahead and made a whole breakup playlist",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qf09d64bb38",
  "kind": "yes/no",
  "text": "Claim: Tothill Fields was an 18th-century area of Westminster in the county of Middlesex, a historic county in south-east region of England that ceased to exist in 1790.\n\nPassages:\n\n[Tothill Fields]\nTothill Fields was an 18th-century area of Westminster in the county of Middlesex that lay south of St James's Park on the north bank of the river Thames.\n\n[Middlesex]\nMiddlesex ( , abbreviation: Middx) is a historic county in south-east England.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 }
]
