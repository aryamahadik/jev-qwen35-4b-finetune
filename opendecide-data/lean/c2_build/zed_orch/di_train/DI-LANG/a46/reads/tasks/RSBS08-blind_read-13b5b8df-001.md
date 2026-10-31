# A46 replay label-noise blind read RSBS08-blind_read-13b5b8df-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS08-blind_read-13b5b8df-001.json

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
  "qid": "q0c2b6ff192",
  "kind": "yes/no",
  "text": "Tweet: tex-mex restaurants that stop serving breakfast tacos after 10:30/11 am are the reason i have trust issues",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q7afa121cf6",
  "kind": "yes/no",
  "text": "Claim: The film where Dan Shor plays Ram, stars Jeff Bridges as a programmer, not The Million Dollar Duck.\n\nPassages:\n\n[Dan Shor]\nHis most recognized roles include Ram in \"Tron\" (1982) and Billy the Kid in \"Bill & Ted's Excellent Adventure\" (1989).\n\n[The Million Dollar Duck]\nThe Million Dollar Duck (also titled as The $1,000,000 Duck) is a 1971 American comedy film produced by Walt Disney Productions about a goose that lays golden eggs scenario.\n\n[Tron]\nTron is a 1982 American science fiction action-adventure film written and directed by Steven Lisberger, based on a story by Lisberger and Bonnie MacBird and produced by Walt Disney Productions. The film stars Jeff Bridges as a computer programmer who is transported inside the software world of a mainframe computer where he interacts with programs in his attempt to escape.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q279ed78dbc",
  "kind": "yes/no",
  "text": "Claim: The MTV Europe Music Award for Best Song was first awarded for a song performed by Youssou N'Dour and Neneh Cherry.\n\nPassages:\n\n[MTV Europe Music Award for Best Song]\nIt was first awarded in 1994, when \"7 Seconds\" won it, and has been given out since.\n\n[7 Seconds (song)]\nIt was released in 1994 as a single performed by Youssou N'Dour and Neneh Cherry.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qdd86d12b01",
  "kind": "yes/no",
  "text": "Claim: The Metallica co-founder James Hetfield wrote the power ballad lyrics to \"Mama Said\" on the back of a paper napkin.\n\nPassages:\n\n[Mama Said (Metallica song)]\n\"Mama Said\" is a power ballad by American heavy metal band Metallica from their sixth album \"Load\", with music and lyrics by James Hetfield (music credited to Hetfield/Ulrich).\n\n[James Hetfield]\nHetfield co-founded Metallica in October 1981 after answering a classified advertisement by drummer Lars Ulrich in the Los Angeles newspaper \"The Recycler\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q9c4d2786a7",
  "kind": "yes/no",
  "text": "Claim: Bambi, is based on a book by the American author Felix Salten, The Country Bears is not.\n\nPassages:\n\n[Bambi]\nBambi is a 1942 American animated film directed by David Hand (supervising a team of sequence directors), produced by Walt Disney and based on the book \"Bambi, a Life in the Woods\" by Austrian author Felix Salten.\n\n[The Country Bears]\nThe Country Bears is a 2002 American family musical comedy film, directed by Peter Hastings, produced by Walt Disney Pictures, and based on the Disney theme park attraction \"Country Bear Jamboree\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q0b90e11a84",
  "kind": "yes/no",
  "text": "Claim: The series containing \"Moe Goes from Rags to Riches\" as the third episode of its twenty-third season, released an episode that aired on February 19, 2012 entitled \"At Long Last Leave\", representing the show's 500th episode milestone.\n\nPassages:\n\n[The Simpsons (season 23)]\n\"The Simpsons\"' twenty-third season began airing on Fox on September 25, 2011, and ended May 20, 2012. The show's 500th episode, \"At Long Last Leave\", aired February 19, 2012.\n\n[Moe Goes from Rags to Riches]\n\"Moe Goes from Rags to Riches\" is the twelfth episode of the twenty-third season of the American animated sitcom \"The Simpsons\".\n\n[At Long Last Leave]\n\"At Long Last Leave\" is the fourteenth episode of \"The Simpsons\"' twenty-third season, and the 500th episode overall of the series.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q59d7b9d1fc",
  "kind": "yes/no",
  "text": "Claim: The host of Australia's Got Talent was born in Warrnambool, Victoria.\n\nPassages:\n\n[Australia's Got Talent (season 8)]\nMorris did not return as host as she is committed to another show and was replaced by Dave Hughes as the host.\n\n[Dave Hughes]\nDavid William \"Hughesy\" Hughes (born 26 November 1970 in Warrnambool, Victoria) is an Australian stand-up comedian, and a radio and television presenter.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qa5e05ebbf1",
  "kind": "yes/no",
  "text": "Claim: Michael W. Wright was CEO of this American retailing company from 1981 to 2001. This company supplied Festival's private label brands.\n\nPassages:\n\n[Festival Foods]\nFestival's private label brands are supplied by SuperValu, with the majority under their Essential Everyday label.\n\n[SuperValu (United States)]\nSuperValu, Inc. is an American retailing company.\n\n[Michael W. Wright]\nHe has served as chief executive officer of SuperValu (1981–2001) and who currently is a director of Wells Fargo & Company.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q68e35c16c9",
  "kind": "yes/no",
  "text": "Claim: Rebecca Rippy, born in May 1977, shared the stage with an American bluegrass singer, songwriter, and multi-instrumentalist known as the \"the new Queen of Bluegrass\".\n\nPassages:\n\n[Rhonda Vincent]\nRhonda Lea Vincent (born July 13, 1962) is an American bluegrass singer, songwriter, and multi-instrumentalist.\n\n[Rebecca Rippy]\nRebecca Rippy (born 1977) is an American singer/songwriter, most notably in the roots country and Americana genres. She has played or shared the stage with such well-known acts and artists as REM producer Don Dixon, Leon Russell, Lucy Kaplansky, Tony Rice, Donna the Buffalo, Jim Lauderdale, Bill Mallonee and the Vigilantes of Love, blues legend Tinsley Ellis, John Cowan, Rhonda Vincent, Danielle Howle, and Old Crow Medicine Show, and has become a regular performer at such prestigious songwriter venues as the Bluebird Café in Nashville, TN, and at the Neighborhood Theater in Charlotte, NC.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q9ada3a02f4",
  "kind": "yes/no",
  "text": "Claim: One of the stars of the film Nos Miran acted in the 1986 movie that Emmanuelle Béart won the César Award for Best Supporting Actress. That movie was directed by Claude Berri.\n\nPassages:\n\n[Emmanuelle Béart]\nAn eight-time César Award nominee, she won the César Award for Best Supporting Actress for the 1986 film \"Manon des Sources\".\n\n[Manon des Sources (1986 film)]\nManon des Sources (] ; meaning Manon of the Spring) is a 1986 French language film. Directed by Claude Berri, it is the second of two films adapted from the 1966 two-volume novel by Marcel Pagnol, who wrote it based on his own earlier film of the same title.\n\n[Margarita Lozano]\nShe has worked for Luis Buñuel in \"Viridiana\", Sergio Leone in \"A Fistful of Dollars\", Pier Paolo Pasolini in \"Pigsty\", the Taviani brothers in \"The Night of the Shooting Stars\", \"Kaos\" and \"Good Morning Babylon\"; Nanni Moretti in \"La messa è finita\"; and in Claude Berri's diptych \"Jean de Florette\" and \"Manon of the Spring\".\n\n[Nos miran]\nIt is a thriller starring Carmelo Gómez with Iciar Bollain, Margarita Lozano and Francisco Algora.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q78935478a5",
  "kind": "yes/no",
  "text": "Text: Humans are the only animal that can’t tell fantasy from reality",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qa83f7d67b0",
  "kind": "yes/no",
  "text": "Text: I love to pick my modules on a first come first served basis at the same time as everyone in my entire year on a website that hasn’t been updated since 1995 . Thrilling ❤️",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qb9fa12e65d",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Claires, you should not do full hysterectomies.",
   "yo @claires do yall do hysterectomies?"
  ]
 },
 {
  "qid": "q0c151079d9",
  "kind": "yes/no",
  "text": "Claim: Wharton appeared as The Hippy in a comedy film written and produced by Martin McDonagh.\n\nPassages:\n\n[Richard Wharton (actor)]\nWharton began his career in 1986 in the film \"Running Scared\". In 2012, he appeared as The Hippy in \"Seven Psychopaths\".\n\n[Seven Psychopaths]\nSeven Psychopaths is a 2012 British-American crime black comedy film written and directed by Martin McDonagh.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc0040fc9b6",
  "kind": "yes/no",
  "text": "Claim: Baker's Haulover Inlet is part of a larger area located just north of the road. The Whitman family own an upscale shopping mall in Atlanta known for luxury retail on the same road.\n\nPassages:\n\n[Bal Harbour Shops]\nBal Harbour Shops is owned by the Whitman family and is one of the few remaining family-owned malls in the nation.\n\n[Haulover Park]\nThe park is located on a shoal between the Atlantic Ocean and Biscayne Bay, just north of the Broad Causeway (SR 922) and Collins Avenue.\n\n[Baker's Haulover Inlet]\nIt is the location of an official nude beach, recreation areas and marina in the 99-acre Haulover Park.\n\n[Florida State Road 922]\nThe street is an important commercial artery in northeastern Miami-Dade County, with stores lining much of the route, including the Bal Harbour Shops mall near its eastern terminus.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qcf50d428b5",
  "kind": "yes/no",
  "text": "Claim: Both the director of Mulholland Falls and Robert Redford work as a director and film producer.\n\nPassages:\n\n[Mulholland Falls]\nMulholland Falls is a 1996 American neo-noir crime thriller film directed by Lee Tamahori, written by Pete Dexter, and starring an ensemble cast featuring Nick Nolte, Jennifer Connelly, Chazz Palminteri, Michael Madsen, Chris Penn, Melanie Griffith, Andrew McCarthy, Treat Williams, and John Malkovich.\n\n[Robert Redford]\nCharles Robert Redford Jr. (born August 18, 1936) is an American actor, director, producer, businessman, environmentalist, and philanthropist.\n\n[Lee Tamahori]\nLee Tamahori (born 17 June 1950) is a New Zealand filmmaker best known for directing 1994 film \"Once Were Warriors\" and 2002 James Bond film \"Die Another Day\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q5b58445ba6",
  "kind": "yes/no",
  "text": "Claim: The developer of origami technique Wet-folding was given the Order of the Rising Sun, 5th class, award. The award was given by Hirohito during the Shōwa era in first century Japanese history.\n\nPassages:\n\n[Hirohito]\nThe word \"Shōwa\" is the name of the era that corresponded with the Emperor's reign, and was made the Emperor's own name upon his death.\n\n[Akira Yoshizawa]\nIn 1983, Emperor Hirohito awarded him the Order of the Rising Sun, 5th class, one of the highest honors bestowed in Japan.\n\n[Wet-folding]\nWet-folding is an origami technique developed by Akira Yoshizawa that employs water to dampen the paper so that it can be manipulated more easily.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qcba098798a",
  "kind": "yes/no",
  "text": "Claim: High Plains is a place that has both Lano Estacado and this kind of geological rock formations. The Woodbine Foundation overlies this area.\n\nPassages:\n\n[Woodbine Formation]\nThe Woodbine overlies the Maness Shale, Buda Limestone, or older rocks, and underlies the Eagle Ford Group or Austin Chalk.\n\n[High Plains (United States)]\nThe southern region of the Western High Plains ecology region contains the geological formation known as Llano Estacado which can be seen from a short distance or from on satellite maps.\n\n[Buda Limestone]\nThe Buda Limestone is a geological formation in the High Plains and Trans-Pecos regions of West Texas whose strata date back to the Late Cretaceous.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qa2f19d91a2",
  "kind": "yes/no",
  "text": "Claim: On November 2, 2010, John Spratt lost to an AMerican politician who served in the South Carolina General Assembly from 2007 until 2011.\n\nPassages:\n\n[Mick Mulvaney]\nJohn Michael Mulvaney ( ; born July 21, 1967) is an American politician in the Republican Party and Director of the Office of Management and Budget (OMB). Mulvaney served in the South Carolina General Assembly from 2007–2011, first in the State House of Representatives and then the State Senate.\n\n[John Spratt]\nOn November 2, 2010, he lost to Republican challenger Mick Mulvaney.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qfab35cafba",
  "kind": "yes/no",
  "text": "Claim: The proper name of the husband of Lollia Paullina was Gaius Julius Caesar Augustus Germanicus.\n\nPassages:\n\n[Lollia Paulina]\nLollia Paulina, also known as Lollia Paullina (15-49) was a Roman Empress for six months in 38 as the third wife and consort of the Roman emperor Caligula.\n\n[Caligula]\nCaligula ( ), properly Gaius Julius Caesar Augustus Germanicus (31 August AD 12 – 24 January AD 41) was Roman emperor from AD 37–41.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q258ab041ac",
  "kind": "yes/no",
  "text": "Post: @majornelson Sounds like a strong contender for GOTY",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qf1d748ce6d",
  "kind": "yes/no",
  "text": "Claim: The award winning game Doom is a reboot of the franchise developed by id Software.\n\nPassages:\n\n[2016 in video gaming]\nMany awards went to games such as \"Overwatch\", \"\", \"Inside\", \"Doom\", \"Dark Souls III\", \"The Last Guardian\", \"Dishonored 2\" and \"Titanfall 2\".\n\n[Doom (2016 video game)]\nA reboot of the \"Doom\" franchise, it is the fourth title in the main series and the first major installment since \"Doom 3\" in 2004.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qfb7f4db80f",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "I’m not exciting to start this job",
   "So excited to start this job!😊"
  ]
 },
 {
  "qid": "qb726f4eca4",
  "kind": "yes/no",
  "text": "Tweet: Is this first Cybex isokinetic dynamometer? @DrAndrewBateman #PRS2021",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q16818c9c7c",
  "kind": "yes/no",
  "text": "Claim: Marjorie McGinnis was the original female founder of the brewery that was purchased in 2006 by the largest brewery in the state of Taiwan.\n\nPassages:\n\n[Frederick Brewing Company]\nIt was founded sometime between 1992 and 1993 by Marjorie McGinnis, Kevin Brannon, and Steve Nordahl and had its grand opening on 12 February 1997. In early 2002 or 2003 the company was placed into receivership and in 2006 was purchased by Flying Dog Brewery and renamed Wild Goose Brewery.\n\n[Flying Dog Brewery]\nFounded in 1990 by George Stranahan and Richard McIntyre, it is the largest brewery in Maryland.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qcbf31aa3ce",
  "kind": "yes/no",
  "text": "Claim: The company who produces Fangoria's Weekend of Horrors is located in a city with an estimated 2014 population of 200,167.\n\nPassages:\n\n[Fangoria's Weekend of Horrors]\nFormerly produced in partnership with Creation Entertainment, the Weekend of Horrors show is now owned exclusively by \"Fangoria Magazine\" and is held once annually in Los Angeles, California.\n\n[Glendale, California]\nIts estimated 2014 population was 200,167, making it the third largest city in Los Angeles County and the 23rd-largest city in California.\n\n[Creation Entertainment]\nCreation Entertainment is an American for-profit entertainment company located in Glendale, California, which produces fan conventions for fans of various films and television series, mainly in the science fiction, horror, and fantasy genres.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q668dd4086f",
  "kind": "yes/no",
  "text": "Claim: The 1926 Princeton Tigers football team only lost to one team. That team was located in Maryland.\n\nPassages:\n\n[1926 Navy Midshipmen football team]\nThe 1926 Navy Midshipmen football team represented the United States Naval Academy in the 1926 college football season.\n\n[1926 Princeton Tigers football team]\nThe Tigers' sole loss of the season was to Navy by a 27–13 score.\n\n[United States Naval Academy]\nThe United States Naval Academy (also known as USNA, Annapolis, or simply Navy) is a four-year coeducational federal service academy in Annapolis, Maryland.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q921f794d35",
  "kind": "yes/no",
  "text": "Text: Praying this works out for me🙏🏼",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q8449568fde",
  "kind": "yes/no",
  "text": "Claim: The highway that goes over the New York State Route 102 connects to the Southern State Parkway in a community with a population of over 10,000.\n\nPassages:\n\n[New York State Route 102]\nNY 102 goes under the Meadowbrook State Parkway, but has no connecting ramps to or from the parkway.\n\n[Meadowbrook State Parkway]\nThe parkway heads north, crossing South Oyster Bay and intersecting Loop Parkway before crossing onto the mainland and connecting to the Southern State Parkway in North Merrick.\n\n[North Merrick, New York]\nThe population was 12,272 at the 2010 census.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qae3b9bc9ee",
  "kind": "yes/no",
  "text": "Claim: I Get Off is the first single from debut album of the hard rock band. This band and the band who released Hebrews (album) are from different states.\n\nPassages:\n\n[I Get Off]\n\"I Get Off\" is the first single released by the hard rock band, Halestorm.\n\n[Halestorm]\nHalestorm is an American hard rock band from Red Lion, Pennsylvania, consisting of lead vocalist and guitarist Lzzy Hale, her brother drummer and percussionist Arejay Hale, guitarist Joe Hottinger, and bassist Josh Smith.\n\n[Say Anything (band)]\nSay Anything is an American rock band from Los Angeles, California.\n\n[Hebrews (album)]\nHebrews is the sixth full-length studio album by American rock band Say Anything.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q73e79e9ff9",
  "kind": "yes/no",
  "text": "Text: Big day in the Mumford house #sports day",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q9335c93e4c",
  "kind": "yes/no",
  "text": "Claim: Of singers Kenny Greene and Billy Idol Kenny Greene is younger.\n\nPassages:\n\n[Kenny Greene]\nKenny Greene (January 17, 1969 – October 1, 2001) was an American singer-songwriter who was also a member of the R&B group Intro.\n\n[Billy Idol]\nWilliam Michael Albert Broad (born 30 November 1955), known professionally as Billy Idol, is an English musician, singer, songwriter, and actor.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qcb165dd9a1",
  "kind": "yes/no",
  "text": "Claim: The founder of a nonprofit organization located in Mary's Harbour acts as a missionary to Newfoundland and Labrador.\n\nPassages:\n\n[Mary's Harbour]\nThe International Grenfell Association decided to relocate its hospital and boarding school, destroyed by the fire, from Battle Harbour to Mary's Harbour.\n\n[Wilfred Grenfell]\nSir Wilfred Thomason Grenfell, KCMG (28 February 1865 – 9 October 1940) was a medical missionary to Newfoundland and Labrador.\n\n[International Grenfell Association]\nThe International Grenfell Association (IGA) is an organization founded by Sir Wilfred Grenfell to provide health care, education, religious services, and rehabilitation and other social activities to the fisherman and coastal communities in northern Newfoundland and the coast of Labrador.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q86872386af",
  "kind": "yes/no",
  "text": "Claim: Queen Elizabeth II is the mother of Prince Charles, who had allegations made against him related to the lawsuit \"Two Jane Does v US\".\n\nPassages:\n\n[Two Jane Does v US]\nJane Doe #1 and Jane Doe #2 vs United States of America is a civil action in the US District Court in Florida, which has led to allegations of inappropriate behavior being made against Alan Dershowitz and Prince Andrew, Duke of York.\n\n[Prince Andrew, Duke of York]\nPrince Andrew, Duke of York, {'1': \", '2': \", '3': \", '4': \"} (Andrew Albert Christian Edward, born 19 February 1960), is the second son and third child of Queen Elizabeth II and Prince Philip, Duke of Edinburgh.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q676d613411",
  "kind": "yes/no",
  "text": "Claim: Brady Seals has released more solo albums than the entertainer who Avril Lavigne featured on the song Get Over Me with.\n\nPassages:\n\n[Get Over Me]\n\"Get Over Me\" is a song by American singer and songwriter Nick Carter featuring Canadian singer Avril Lavigne.\n\n[Brady Seals]\nBrady Seals (born March 29, 1969) is an American country music artist. A fourth solo album, \"Play Time\", was released in 2009 via Star City.\n\n[Nick Carter (musician)]\nNickolas Gene \"Nick\" Carter (born January 28, 1980) is an American singer, songwriter, actor, and dancer. As of 2015, Carter has released three solo albums, \"Now or Never\", \"I'm Taking Off\" and \"All American\" during breaks between Backstreet Boys schedules, and a collaboration with Jordan Knight titled \"Nick & Knight\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q3ac7ebdf71",
  "kind": "yes/no",
  "text": "Claim: Paul McCartney wrote a duo's biggest hit. That hit was covered by Del Davis, featured on \"Mellow Dubmarine\". Norman Newell was an Abbey Road Studios manager for the duo.\n\nPassages:\n\n[A World Without Love]\nThe song was written by Paul McCartney and attributed to Lennon–McCartney.\n\n[Norman Newell]\nAs an A&R manager for EMI he worked with musicians such as Shirley Bassey, Claude François, Vera Lynn, Russ Conway, Bette Midler, Judy Garland, Petula Clark, Jake Thackray, Malcolm Roberts, Bobby Crush and Peter and Gordon.\n\n[Del Davis (singer)]\nHis cover of \"World Without Love\" was featured on \"Mellow Dubmarine\".\n\n[Gordon Waller]\nGordon Trueman Riviere Waller (4 June 1945 – 17 July 2009) was a British singer–songwriter–guitarist, best known as Gordon of the 1960s pop music duo Peter and Gordon, whose biggest hit was the No. 1 million-selling classic \"A World Without Love\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q922f198217",
  "kind": "yes/no",
  "text": "Claim: Chess is more popular around the world than the most popular game designed by Leo Colovini.\n\nPassages:\n\n[Chess]\nChess is a two-player strategy board game played on a chessboard, a checkered gameboard with 64 squares arranged in an 8×8 grid. The game is played by millions of people worldwide.\n\n[Leo Colovini]\nHis most popular game is \"Cartagena\".\n\n[Cartagena (board game)]\nCartagena is a critically acclaimed German-style board game released in 2000, that takes as its theme the legendary 1672 pirate-led jailbreak from the dreaded fortress of Cartagena.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe5374164d6",
  "kind": "yes/no",
  "text": "Post: We have changed our name on here to keep family from finding us, we are still didivination just look different.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q4a06b92b97",
  "kind": "yes/no",
  "text": "Claim: ORO VAMTAC is the vehicle made by UROVESA that is most like the four-wheel drive military light truck produced by AM General.\n\nPassages:\n\n[Humvee]\nThe High Mobility Multipurpose Wheeled Vehicle (HMMWV), commonly known as the Humvee, is a four-wheel drive military light truck produced by AM General.\n\n[UROVESA]\nURO, Vehículos Especiales, S.A. (UROVESA) is a Spanish heavy vehicle manufacturer based in Santiago de Compostela, Galicia. It is best known for the production of the URO VAMTAC, a Humvee-like four-wheel drive motor vehicle, and URO trucks.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q7c1105e0fe",
  "kind": "yes/no",
  "text": "Post: @WalesOnline Riveting news.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q2f8a60228d",
  "kind": "yes/no",
  "text": "Claim: Television station KCTV, licensed to Kansas City, Missouri, is adjacent to another television station. This other television station aired the 25-minute programme \"Check Please!\".\n\nPassages:\n\n[KCPT]\nOwned by Public Television 19, Inc., KCPT maintains studio facilities (which are shared with sister adult album alternative radio station KTBG (90.9 FM)) located on East 31st Street in Kansas City, Missouri's Union Hill section (adjacent to the transmitter tower of CBS affiliate KCTV (channel 5)), and its transmitter is located near 23rd Street and Stark Avenue in Kansas City, Missouri's Blue Valley section.\n\n[KCTV]\nKCTV, virtual channel 5 (UHF digital channel 24), is a CBS-affiliated television station licensed to Kansas City, Missouri, United States and also serving Kansas City, Kansas.\n\n[Check, Please!]\nKansas City then began airing on KCPT in 2009, and Check, Please!",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q4327899ff0",
  "kind": "yes/no",
  "text": "Text: Entry level jobs that require 3 years prior experience 💕💕 ly 💕💕",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q05e8c24033",
  "kind": "yes/no",
  "text": "Claim: The actor who starred, along with Go Ah-sung, in the South-Korean comedy film, Office, appeared in The Deal. The Deal was directed by Son Yong-ho.\n\nPassages:\n\n[Park Sung-woong]\nPark Sung-woong (born January 9, 1973) is a South Korean actor. Following his acting debut in \"No. 3\" in 1997, Park has starred in several movies and television series, notably as a gangster in \"New World\" (2013) and a serial killer in \"The Deal\" (2015).\n\n[Office (2015 South Korean film)]\nOffice (오피스 ) is 2015 South Korean slasher-thriller film directed by Hong Won-chan and starring Go Ah-sung and Park Sung-woong.\n\n[The Deal (2015 film)]\nThe Deal (; lit.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5739333971",
  "kind": "yes/no",
  "text": "Claim: 1: Parnassius nordmanni is a high altitude butterfly which is found the Caucasus. 2:The larva feeds on a species including \"C. alpestris\", \"C. conorhiza\" and \"C. emanueli\". 3:That species and Cedrus are classified as genus in the naming system.\n\nPassages:\n\n[Corydalis]\nCorydalis (Greek \"korydalís\" \"crested lark\") is a genus of about 470 species of annual and perennial herbaceous plants in the Papaveraceae family, native to the temperate Northern Hemisphere and the high mountains of tropical eastern Africa.\n\n[Parnassius nordmanni]\nThe larva feeds on \"Corydalis\" species including \"C. alpestris\", \"C. conorhiza\" and \"C. emanueli\".\n\n[Cedrus]\nCedrus (common English name cedar) is a genus of coniferous trees in the plant family Pinaceae.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q062df24d57",
  "kind": "yes/no",
  "text": "Claim: The home of F.C. Daburiyya is east of a city where 30.9% of its citizens are Christian.\n\nPassages:\n\n[Nazareth]\nNazareth ( ; Hebrew: נָצְרַת‎ , \"Natzrat\"; Arabic: النَّاصِرَة‎ ‎ , \"an-Nāṣira\"; Aramaic: ܢܨܪܬ‎ ‎ , \"Naṣrath\") is the capital and the largest city in the Northern District of Israel. The inhabitants are predominantly Arab citizens of Israel, of whom 69% are Muslim and 30.9% Christian.\n\n[Daburiyya]\nDaburiyya (Arabic: دبورية‎ ‎ ; Hebrew: דַבּוּרִיָּה‎ ), also \"Deburieh\" or \"Dabburieh\", is an Arab village ca. 8 km. east of Nazareth in Israel's Northern District.\n\n[F.C. Daburiyya]\nF.C. Daburiyya (Hebrew: מועדון ספורט דבוריה אוסמה‎ ‎ ), also known as Hapoel Daburiyya (Hebrew: הפועל דבוריה‎ ‎ ; Arabic: هبوعيل دبورية‎ ‎ ), is an Israeli football club based in Daburiyya.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q5982f75c55",
  "kind": "yes/no",
  "text": "Claim: Verona directed the 1979 American drama film that starred the actress who won the Golden Globe Award for Best Supporting Actress for \"Psycho\".\n\nPassages:\n\n[Boardwalk (film)]\nBoardwalk is a 1979 American drama film written by Stephen Verona and Leigh Chapman and directed by Verona.\n\n[Janet Leigh]\nShe is best remembered for her performance in \"Psycho\", for which she was awarded the Golden Globe Award for Best Supporting Actress and received an Academy Award nomination.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q49505905d8",
  "kind": "yes/no",
  "text": "Text: Happy happy happy https://t.co/9W1XIbpL6x",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q1b2f17e939",
  "kind": "yes/no",
  "text": "Claim: The album produced by John Leckie and engineered by Junun features artwork by the same person who did the artwork for another of the band's albums, Johnny Greenwood is the Controller. Planet Telex is the opening track on this album.\n\nPassages:\n\n[The Bends]\nThe Bends (stylised as the bends) is the second studio album by the English alternative rock band Radiohead, released on 13 March 1995 by Parlophone Records in the United Kingdom and by Capitol Records in the United States. The album was produced by John Leckie and engineered by Nigel Godrich, who would go on to co-produce all future albums by the band.\n\n[Jonny Greenwood Is the Controller]\nJonny Greenwood Is the Controller is a compilation album created by Jonny Greenwood of Radiohead and released on Trojan Records. The album features artwork by Stanley Donwood, who has provided art for every Radiohead album since \"The Bends\" (1995).\n\n[Planet Telex]\n\"Planet Telex\" is a song written by Radiohead and is the opening track of their 1995 album \"The Bends\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qd27833f10e",
  "kind": "yes/no",
  "text": "Claim: William Hopke played the 1909 Cuban-American Major League Clubs Series, for the Cleveland Indians, the team Erik Sabel played for in 2002, which were founded in 1901.\n\nPassages:\n\n[Erik Sabel]\nHe played for the Arizona Diamondbacks in 1999 and 2001 and the Detroit Tigers in 2002.\n\n[Detroit Tigers]\nOne of the AL's eight charter franchises, the club was founded in Detroit in 1901 .\n\n[Bill Hopke]\nWilliam \"Silent Bill\" Hopke (November 2, 1881 – April 18, 1959) was an American professional baseball player. Hopke also played in the 1909 Cuban-American Major League Clubs Series for the Detroit Tigers, though he never played in a major league game for Detroit.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q958206d8e0",
  "kind": "yes/no",
  "text": "Claim: Marty Stratton became responsible for the overall development of an award winning game. This award winning game is a reboot of the franchise developed by id Software.\n\nPassages:\n\n[2016 in video gaming]\nMany awards went to games such as \"Overwatch\", \"\", \"Inside\", \"Doom\", \"Dark Souls III\", \"The Last Guardian\", \"Dishonored 2\" and \"Titanfall 2\".\n\n[Doom (2016 video game)]\nA reboot of the \"Doom\" franchise, it is the fourth title in the main series and the first major installment since \"Doom 3\" in 2004.\n\n[Marty Stratton]\nIn 2006, he became responsible for the overall development of \"Quake Live\", \"Rage\", and \"Doom\" with ZeniMax Media and Bethesda Softworks respectively.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 }
]
