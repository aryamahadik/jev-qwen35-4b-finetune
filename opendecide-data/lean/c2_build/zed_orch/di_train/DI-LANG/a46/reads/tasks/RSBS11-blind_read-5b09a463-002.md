# A46 replay label-noise blind read RSBS11-blind_read-5b09a463-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS11-blind_read-5b09a463-002.json

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
  "qid": "q8485757898",
  "kind": "yes/no",
  "text": "Claim: Charlie Murphy, brother of Eddie Murphy, starred in Twisted Fortune directed by Victor Varnada.\n\nPassages:\n\n[Charlie Murphy]\nHe was the older brother of comedian Eddie Murphy.\n\n[Twisted Fortune]\nTwisted Fortune is a black comedy about a bumbling small-time crook (played by Charlie Murphy) who finds a bottle cap worth $1,000,000 while robbing a convenience store. It was directed by comedian Victor Varnado (\"End of Days\"), who also acted in the movie.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q9694bc24aa",
  "kind": "yes/no",
  "text": "Tweet: i would rather be outside reed timmers car in f3 tornado winds than go to work today",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q39aecfcb04",
  "kind": "yes/no",
  "text": "Claim: Steven Earl \"Steve\" Gaines is the guitarist that played on the LP, which included \"That Smell\" released in 1977, and was a member of an American Southern Rock band from May 1976 until his death Oct 1977.\n\nPassages:\n\n[Steve Gaines]\nSteven Earl \"Steve\" Gaines (September 14, 1949 – October 20, 1977) was an American musician. He is best known as a guitarist, vocalist and songwriter of Southern rock band Lynyrd Skynyrd from May 11, 1976 until his death on October 20, 1977 and is the younger brother of Cassie Gaines, who was a back up vocalist for the band's live performances.\n\n[Street Survivors]\nStreet Survivors is the fifth studio album by Southern rock band, Lynyrd Skynyrd, released on October 17, 1977. The LP is the last Skynyrd album recorded by original members Ronnie Van Zant and Allen Collins, and is the sole Skynyrd studio recording by guitarist Steve Gaines.\n\n[That Smell]\nWritten by Ronnie Van Zant and guitarist Allen Collins, it was released in 1977 on the album \"Street Survivors\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3fa225ad29",
  "kind": "yes/no",
  "text": "Claim: Tales of Tahoe Tessie state that the creature resides in an underwater tunnel. According to the 2010 census, the population of the town located approximately seven miles south of that underwater tunnel was 842.\n\nPassages:\n\n[Cave Rock Tunnel]\nThe Cave Rock Tunnel is a dual bore highway tunnel on U.S. Route 50 (US 50) along the eastern shore of Lake Tahoe approximately seven miles (11.4 km) north of Stateline, in Douglas County, Nevada, United States.\n\n[Tahoe Tessie]\nTales of the lake-dwelling creature can be traced to stories told by members of the Washoe and Paiute tribes in the mid-19th century, stating that the creature resides in an underwater tunnel beneath Cave Rock, and sightings have continued into modern day.\n\n[Stateline, Nevada]\nThe population was 842 at the 2010 census.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q1324e277fe",
  "kind": "yes/no",
  "text": "Claim: Peter Straub is a romance novelist. The author of The Playmaker is also a novelist.\n\nPassages:\n\n[Peter Straub]\nPeter Francis Straub (born March 2, 1943) is an American novelist and poet.\n\n[Thomas Keneally]\nThomas Michael Keneally, AO (born 7 October 1935) is a prolific Australian novelist, playwright, and essayist.\n\n[The Playmaker]\nThe Playmaker is a novel based in Australia written by the Australian author Thomas Keneally.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q71749d1fe5",
  "kind": "yes/no",
  "text": "Claim: The WAMC public radio network in New York has not allowed Eric Plakun to dis his psychiatric work.\n\nPassages:\n\n[Eric Plakun]\nEric M. Plakun, MD, DLFAPA, FACPsych, is an American board certified psychiatrist, psychoanalyst, researcher and forensic psychiatrist. Plakun has been widely published and quoted in the media on psychotherapy and psychiatry, including in The New York Times and The Globe and Mail. He has appeared in the media to discuss his psychiatric work on WAMC, the Albany, New York affiliate of NPR.\n\n[WAMC]\nWAMC is a public radio network headquartered in Albany, New York.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qaccb23bc8c",
  "kind": "yes/no",
  "text": "Claim: The film that featured Nico Liersch in the role of Winnie Markus was directed by same director of the film About a Girl. That film is based on a book by Markus Zusak.\n\nPassages:\n\n[About a Girl (2001 film)]\nAbout a Girl is a nine-minute short film directed by Brian Percival.\n\n[Brian Percival]\nBrian Percival is a British film director, known for his work on the British television series \"Downton Abbey\" and \"North & South\", as well as the feature film \"The Book Thief\".\n\n[Nico Liersch]\nHe is mostly known for his role as Rudy Steiner in the 2013 film \"The Book Thief\".\n\n[The Book Thief (film)]\nThe film is based on the 2005 novel \"The Book Thief\" by Markus Zusak and adapted by Michael Petroni.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qdb6d215071",
  "kind": "yes/no",
  "text": "Claim: The actor that plays Joe MacMillan in \"Halt and Catch Fire\" also starred with Scott Glenn in the 2017 horror film The Keeping Hours.\n\nPassages:\n\n[Lee Pace]\nHe currently stars as protagonist Joe MacMillan in AMC's \"Halt and Catch Fire\".\n\n[The Keeping Hours]\nThe Keeping Hours is a 2017 American supernatural romantic horror film directed by Karen Moncrieff and written by Rebecca Sonnenshine. The film stars Lee Pace and Carrie Coon.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qf4ae3b2449",
  "kind": "yes/no",
  "text": "Text: love when the train stops in philly and everybody boards and of a sudden it smells like a ham sandwich",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qad73da121c",
  "kind": "yes/no",
  "text": "Tweet: How is it that I’ve managed 3 months without milking a single cow, then the day before I leave I get roped into a 5am milking??",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qe8a0806d10",
  "kind": "yes/no",
  "text": "Claim: Bernard Blancan received the Best Actor nomination at Cannes in 2006 for the Rachid Bouchareb film Days of Glory.\n\nPassages:\n\n[Days of Glory (2006 film)]\nDays of Glory (French: \"Indigènes - \"Natives\"\" ; Arabic: بلديون‎ ‎ ) is a 2006 French film directed by Rachid Bouchareb.\n\n[Bernard Blancan]\nHe shared the award for Best Actor for his role in \"Days of Glory\" at the 2006 Cannes Film Festival.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qaa8908ba06",
  "kind": "yes/no",
  "text": "Tweet: School psych life if fun because you can feel like complete shit but chances are you have meeting that determines changes in a student’s education that’s bound by legal timelines and took coordination of 6 different schedules and you’re the only one who can run it",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qe199d26e31",
  "kind": "yes/no",
  "text": "Claim: The English former professional footballer who played as a centre-back with Chris Jones, was born by c-section 7 November 1978.\n\nPassages:\n\n[Rio Ferdinand]\nRio Gavin Ferdinand (born 7 November 1978) is an English former professional footballer who played as a centre-back, and current television pundit for BT Sport.\n\n[Chris Jones (footballer, born 1985)]\nChris Jones is a Welsh semi-professional footballer currently playing for Cymru Alliance side Porthmadog. He made several appearances for Leeds and was heavily involved with the first team.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qd3aeca4a10",
  "kind": "yes/no",
  "text": "Claim: This music channel regularly shows the UK R&B Singles and Albums Charts. The media conglomerate owner of this channel (UK and Ireland) changed it's name in 2004. Their new acronym stand for Gesellschaft mit beschränkter Haftung.\n\nPassages:\n\n[Gesellschaft mit beschränkter Haftung]\nA Gesellschaft mit beschränkter Haftung (] , abbreviated GmbH ] and also GesmbH in Austria) is a type of legal entity very common in Germany, Austria, Switzerland (where it is equivalent to a S.à r.l.) and Liechtenstein.\n\n[UK R&amp;B Singles and Albums Charts]\nThe UK R&B chart is also shown regularly on music channels including Kiss, Viva UK, MTV Base and MTV Hits.\n\n[Viva (UK and Ireland)]\nViva (stylised as VIVA) is a music television channel in the United Kingdom and Ireland, owned by VIVA Media and thereby Viacom International Media Networks Europe.\n\n[VIVA Media]\nVIVA Media GmbH (until 2004 \"VIVA Media AG\") is a music television network originating from Germany.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa5ee239f74",
  "kind": "yes/no",
  "text": "Claim: ARA La Gantoise described the captain of the winners of the 1964-65 European Cup Winners Cup as the best defender he had ever played against.\n\nPassages:\n\n[1964–65 European Cup Winners' Cup]\nThe season 1964–65 of the European Cup Winners' Cup football club tournament was won by West Ham United in a final at Wembley Stadium against 1860 Munich. West Ham's Bobby Moore was captaining a side that also included Geoff Hurst and Martin Peters just one season before all three went on to star in England's World Cup winning side of 1966.\n\n[Bobby Moore]\nHe is widely regarded as one of the greatest defenders of all time, and was cited by Pelé as the greatest defender that he had ever played against.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qc1b62f7ffc",
  "kind": "yes/no",
  "text": "Claim: Anthony Sandler is the Chief of Pediatric Surgery at a major hospital. Georgetown University School of Medicine works in association with the hospital that is the largest private hospital in Washington, D.C., not this hospital.\n\nPassages:\n\n[Georgetown University School of Medicine]\nThe School of Medicine works in association with the 609-bed Georgetown University Hospital, Washington Hospital Center, and nine other affiliated federal and community hospitals in the Washington metropolitan area.\n\n[Children's National Medical Center]\nChildren’s National Medical Center (formerly DC Children’s Hospital) is ranked among the top 10 children’s hospitals in the country by \"U.S. News & World Report.\"\n\n[Anthony Sandler]\nAnthony Sandler is the Chief of Pediatric Surgery at Children's National Medical Center, where he also serves as the Principal Investigator in the Children's Research Institute and the Center for Cancer and Immunology Research (CCIR).\n\n[MedStar Washington Hospital Center]\nMedStar Washington Hospital Center is the largest private hospital in Washington, D.C. A member of MedStar Health, the not-for-profit Hospital Center is licensed for 926 beds.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q58ec33d1f4",
  "kind": "yes/no",
  "text": "Claim: The inventor of the Maxim Gun issued 1.9 million shares to Nathan Rothschild.\n\nPassages:\n\n[Maxim Nordenfelt Guns and Ammunition Company]\nThe Maxim-Nordenfelt Guns and Ammunition Company was the result of a takeover by Hiram Maxim of Thorsten Nordenfelt's Nordenfelt Guns and Ammunition Company in 1888. Rothschild issued £1.9 million of shares to finance the merger. Nathan Rothschild retained a substantial shareholding in the new Maxim-Nordenfelt combine and ‘exerted a direct influence over its management’.\n\n[Hiram Maxim]\nHe was the inventor of the Maxim Gun – the first portable, fully automatic machine gun – and held patents on mechanical devices such as a mousetrap, hair-curling irons, and steam pumps.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q1ccef8b289",
  "kind": "yes/no",
  "text": "Claim: This genus, to which Verticordia habrantha is closely related, and Vanilla are derived from the flowers species of plants.\n\nPassages:\n\n[Verticordia habrantha]\nIts hairy sepals are mostly hidden by the round, unfringed petals, and as a result, the plant looks like shrubs in the genus \"Chamelaucium\", to which it is closely related.\n\n[Vanilla]\nVanilla is a flavoring derived from orchids of the genus \"Vanilla\", primarily from the Mexican species, flat-leaved vanilla (\"V. planifolia\").\n\n[Chamelaucium]\nChamelaucium, also known as waxflower, is a genus of shrubs endemic to south western Western Australia. They belong to the myrtle family Myrtaceae and have flowers similar to those of the tea-trees (\"Leptospermum\").",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q587e3e8e35",
  "kind": "yes/no",
  "text": "Claim: Prominent Danish Tibetologist Per Kjeld Sørensen is a professor of Central Asian Studies at the same institution which Josef A. Käs is a professor at. This college was founded by the imperial forces that defeated the Hussite troops at the The Battle of Brüx.\n\nPassages:\n\n[Per K. Sørensen]\nPer Kjeld Sørensen (born 18 December 1950) is a prominent Danish Tibetologist who specialises in Tibetan and Himalayan history, literature and culture.\n\n[Josef A. Käs]\nHe is a Professor at Leipzig University.\n\n[Battle of Brüx]\nThe Hussite troops, led by Jan Želivský, were defeated by the Catholic Imperial forces of Frederick I of Saxony.\n\n[Leipzig University]\nThe university was founded on December 2, 1409 by Frederick I, Elector of Saxony and his brother William II, Margrave of Meissen, and originally comprised the four scholastic faculties.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb05a75811b",
  "kind": "yes/no",
  "text": "Claim: Nick Goldsmith is half of the director/producer duo Hammer & Tongs. The other half and Lee Cheol-ha are both film writers and directors.\n\nPassages:\n\n[Hammer &amp; Tongs]\nHammer & Tongs is the pseudonym of British director and producer duo, promo and film director Garth Jennings and producer Nick Goldsmith, as well as the name of their production company.\n\n[Lee Cheol-ha]\nLee Cheol-ha is a South Korean film director known for his stylish portraits of the human experience.\n\n[Garth Jennings]\nGarth Jennings (born 1972) is a British film director, screenwriter, producer and actor.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qcb8df68110",
  "kind": "yes/no",
  "text": "Claim: Richard Curtis was the breakthrough role for the English Actor starring in Feed the Beast.\n\nPassages:\n\n[Jim Sturgess]\nJames Anthony Sturgess (born 16 May 1981) is an English actor and singer-songwriter. His breakthrough role was appearing as Jude in the musical romance drama film \"Across the Universe\" (2007).\n\n[Feed the Beast]\nFeed the Beast is an American crime drama television series based on the Danish series \"Bankerot\" by Kim Fupz Aakeson and adapted by Clyde Phillips for AMC, starring David Schwimmer and Jim Sturgess.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q013a0d9e7c",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Finally changed out of pajama pants",
   "I changed out of my pajamas today and I think that’s really brave"
  ]
 },
 {
  "qid": "q53245d7431",
  "kind": "yes/no",
  "text": "Claim: Hot Hot Heat and white are both love songs.\n\nPassages:\n\n[1990s (band)]\n1990s were an indie rock three-piece band from Glasgow, Scotland.\n\n[Hot Hot Heat]\nHot Hot Heat was a Canadian indie rock band from Victoria, British Columbia, formed in 1999.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q604dd8b386",
  "kind": "yes/no",
  "text": "Claim: The auditorium where Backstreet Boys: Larger Than Life residency show perfomed at is located in the Planet Hollywood Resort & Casino in Las Vegas, Nevada. This auditorium is located at a hotel and casino owned by the William Jefferson Clinton Federal Building.\n\nPassages:\n\n[Planet Hollywood Las Vegas]\nIt is owned and operated by Caesars Entertainment Corporation.\n\n[The AXIS]\nThe AXIS (known as The AXIS powered by Monster for sponsorship purposes, also referred to as the AXIS Theater) is a mid-sized auditorium located at Planet Hollywood Las Vegas on the Las Vegas Strip.\n\n[Backstreet Boys: Larger Than Life]\nBackstreet Boys: Larger Than Life is the first residency show by American vocal group Backstreet Boys, performed at The AXIS auditorium located in the Planet Hollywood Resort & Casino in Las Vegas, Nevada.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q07108bbed1",
  "kind": "yes/no",
  "text": "Claim: A species related to Xanthosoma and Coronilla are both flowering plants.\n\nPassages:\n\n[Colocasia]\nColocasia is a genus of flowering plants in the family Araceae, native to southeastern Asia and the Indian subcontinent.\n\n[Xanthosoma]\nMany other species (including especially \"X. roseum\") are used as ornamental plants, and in popular horticultural literature are known as ‘ape or elephant ear (from the purported resemblance of the leaf to an elephant's ear), although the latter name is sometimes also applied to members with similar appearance and uses in the closely related genera \"Caladium\", \"Colocasia\" (i.e., taro), and \"Alocasia\".\n\n[Coronilla]\nThe genus Coronilla contains about 20 species of flowering plants native to Europe and North Africa.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q667654c815",
  "kind": "yes/no",
  "text": "Claim: The 1968 documentary film based on Timothy Treadwell premiered before Pray the Devil Back to Hell.\n\nPassages:\n\n[Timothy Treadwell]\nTreadwell's life, work, and death were the subject of Werner Herzog's critically acclaimed documentary film \"Grizzly Man\" (2005).\n\n[Pray the Devil Back to Hell]\nThe film premiered at the 2008 Tribeca Film Festival, where it won the award for Best Documentary.\n\n[Grizzly Man]\nGrizzly Man is a 2005 American documentary film by German director Werner Herzog.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qacb8f1fba4",
  "kind": "yes/no",
  "text": "Claim: Xavier Dolan is the director of the upcoming Candian drama feature film in which the actress who made her film début as the love interest in Wes Anderson's \"The Darjeeling Limited\" stars.\n\nPassages:\n\n[Amara Karan]\nAmara Karan (born 1984) is a Sri Lankan-English actress who made her film début as the love interest in Wes Anderson's \"The Darjeeling Limited\".\n\n[The Death and Life of John F. Donovan]\nThe Death and Life of John F. Donovan is an upcoming Canadian drama film, co-written, co-produced and directed by Xavier Dolan in his English-language debut. It stars Kit Harington, Natalie Portman, Jessica Chastain, Susan Sarandon, Kathy Bates, Jacob Tremblay, Ben Schnetzer, Thandie Newton, Amara Karan, Chris Zylka, Jared Keeso, Emily Hampshire and Michael Gambon.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q95b84c7989",
  "kind": "yes/no",
  "text": "Tweet: The wonderful Rik Mayall would've been 63 today. One half of my favourite sitcom of all time and genuinely delightful, funny and all round beautiful man https://t.co/I7c6Zq2wpx",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q33ffc5440e",
  "kind": "yes/no",
  "text": "Claim: The Laboratory's 60,000 square-foot, university-based campus was located in Maine, United States.\n\nPassages:\n\n[Bigelow Laboratory for Ocean Sciences]\nThe Laboratory's 60,000 square-foot, shore-based campus is located in East Boothbay, Maine, on the Damariscotta River estuary.\n\n[Boothbay Harbor, Maine]\nBoothbay Harbor is a town in Lincoln County, Maine, United States.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q676103f190",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "yeah i enjoy some oregano on a nice pasta dinner (dumps oregano on mac n cheese)",
   "I like to put oregano on my mac and cheese"
  ]
 },
 {
  "qid": "qda7cfc81ea",
  "kind": "yes/no",
  "text": "Claim: More than four and a half million people is the population of the province that Herald Provincial Park is in.\n\nPassages:\n\n[British Columbia]\nBritish Columbia is the westernmost province of Canada, with a population of more than four and a half million people.\n\n[Herald Provincial Park]\nHerald Provincial Park is a provincial park in British Columbia, Canada.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q3843476913",
  "kind": "yes/no",
  "text": "Claim: The city where Giuseppe Sorge was born and Rhodotypos are both types of shrub.\n\nPassages:\n\n[Sutera]\nSutera is a \"comune\" (municipality) in the Province of Caltanissetta in the Italian region Sicily, located about 70 km southeast of Palermo and about 30 km west of Caltanissetta.\n\n[Rhodotypos]\nRhodotypos scandens, the sole species of the genus Rhodotypos, is a deciduous shrub in the family Rosaceae, closely related to \"Kerria\" and included in that genus by some botanists.\n\n[Giuseppe Sorge]\nHe was born in Sutera, Sicily.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf5a06cf989",
  "kind": "yes/no",
  "text": "Tweet: @LittleBigPlanet Thanks for the update. No need to rush take your time :)",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qd1dd33970a",
  "kind": "yes/no",
  "text": "Claim: My Fair Lady is a musical based on this author's play \"Pygmalion\". The author had more influence on turn of the century literature than the writer of Nausea (novel).\n\nPassages:\n\n[My Fair Lady]\nMy Fair Lady is a musical based on George Bernard Shaw's \"Pygmalion\", with book and lyrics by Alan Jay Lerner and music by Frederick Loewe.\n\n[Jean-Paul Sartre]\nJean-Paul Charles Aymard Sartre ( ; ] ; 21 June 1905 – 15 April 1980) was a French philosopher, playwright, novelist, political activist, biographer, and literary critic.\n\n[George Bernard Shaw]\nGeorge Bernard Shaw ( ; 26 July 1856 – 2 November 1950), known at his insistence simply as Bernard Shaw, was an Irish playwright, critic and polemicist whose influence on Western theatre, culture and politics extended from the 1880s to his death and beyond.\n\n[Nausea (novel)]\nNausea (French: \"La Nausée\" ) is a philosophical novel by the existentialist philosopher Jean-Paul Sartre, published in 1938.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1dc9d36153",
  "kind": "yes/no",
  "text": "Claim: The chart that the song Is Anybody Out There? peaked at #14 on is a music industry record chart for a song that is released separately from an album.\n\nPassages:\n\n[Single (music)]\nIn music, a single, record single or music single is a type of release, typically a song recording of fewer tracks than an LP record, an album or an EP record. In most cases, a single is a song that is released separately from an album, although it usually also appears on an album.\n\n[Canadian Hot 100]\nThe Canadian Hot 100 is a music industry record chart in Canada for singles, published weekly by \"Billboard\" magazine.\n\n[Is Anybody Out There?]\nThe single made its chart debut on the Canadian Hot 100 at #67 and peaked at #14.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q28669d0448",
  "kind": "yes/no",
  "text": "Tweet: I miss walking up 3 flights of stairs for class and having to catch my breath in the bathroom 😩",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qf07d8d8c1b",
  "kind": "yes/no",
  "text": "Claim: The art critic that met Joseph Drapell died after the death of Agatha Christie.\n\nPassages:\n\n[Agatha Christie]\nDame Agatha Mary Clarissa Christie, Lady Mallowan, DBE (\"née\" Miller; 15 September 1890 – 12 January 1976) was an English crime novelist, short story writer and playwright.\n\n[Joseph Drapell]\nAt the Cranbrook Academy he met visiting Canadian artist Jack Bush and the American art critic Clement Greenberg, who influenced his work.\n\n[Clement Greenberg]\nClement Greenberg ( ), occasionally writing under the pseudonym K. Hardesh (January 16, 1909 – May 7, 1994), was an American essayist known mainly as an influential visual art critic closely associated with American Modern art of the mid-20th century.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q72fb379933",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "@WilliamShatner Mr Shatner whilst you were sleeping you asked me to join Facebook messenger and then after a polite conversation you then offered me gold necklaces and a singed (sic) tee-shirt - you made my Friday night sir... just awaiting your instructions so I can wire the money...",
   "I would have said it ruined my Friday when I realised that I had been fooled by a Shatner impersonator."
  ]
 },
 {
  "qid": "q08c220c846",
  "kind": "yes/no",
  "text": "Claim: The Lady Craved Excitement was a film that featured the British character actor who was British-born.\n\nPassages:\n\n[The Lady Craved Excitement]\nIt featured Hy Hazell, Michael Medwin and Sid James.\n\n[Sid James]\nSid James (born Solomon Joel Cohen; 8 May 1913 – 26 April 1976) was a South African-born British character actor and comedy actor.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q429f128a76",
  "kind": "yes/no",
  "text": "Claim: The royal title of the man whose totalitarian German government backed the colonization of Poland by German settlers, on of the factors leading to the plight of rural Poland which was the focus of the novel The Outpost was Prince of Bismarck, Duke of Lauenburg.\n\nPassages:\n\n[The Outpost (Prus novel)]\nThe Outpost (Polish title: \"Placówka\") was the first of four major novels by the Polish writer Bolesław Prus. The author, writing in a Poland that had been partitioned a century earlier by Russia, Prussia and Austria, sought to bring attention to the plight of rural Poland, which had to contend with poverty, ignorance, neglect by the country's upper crust, and colonization by German settlers backed by Otto von Bismarck's German government.\n\n[Otto von Bismarck]\nOtto Eduard Leopold, Prince of Bismarck, Duke of Lauenburg (1 April 1815 – 30 July 1898), known as Otto von Bismarck (] ), was a conservative Prussian statesman who dominated German and European affairs from the 1860s until 1890.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q830f8a579a",
  "kind": "yes/no",
  "text": "Claim: The school that The Charles E. Schmidt College of Science is an academic college of is in the US. Another college in the US is the institute where Cecil V. Thomas was the first president of it's predecessor.\n\nPassages:\n\n[Charles E. Schmidt College of Science]\nThe Charles E. Schmidt College of Science is an academic college of Florida Atlantic University located in Boca Raton, Florida, United States.\n\n[Cecil V. Thomas]\nDr. Cecil Vincent \"Tommy\" Thomas September 17, 1892, Perry, Ohio – November 28, 1947, Cleveland, Ohio), was a distinguished American educator, administrator, and the first president of Fenn College.\n\n[Cleveland State University]\nCleveland State University (also known as Cleveland State or CSU) is a public university in downtown Cleveland, Ohio, United States.\n\n[Florida Atlantic University]\nFlorida Atlantic University (also referred to as FAU or Florida Atlantic) is a public university located in Boca Raton, Florida, with five satellite campuses located in the Florida cities of Dania Beach, Davie, Fort Lauderdale, Jupiter, and in Fort Pierce at the Harbor Branch Oceanographic Institution.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc80a1a8a6d",
  "kind": "yes/no",
  "text": "Claim: Thandie Newton is an English actress who starred in the movie \"The Truth About Charlie\".\n\nPassages:\n\n[Thandie Newton]\nMelanie Thandiwe \"Thandie\" Newton ( ; born 6 November 1972) is an English actress.\n\n[The Truth About Charlie]\nThe Truth About Charlie is a 2002 American-French film. The film was produced, directed and co-written by Jonathan Demme, and stars Mark Wahlberg and Thandie Newton in the roles once played by Cary Grant and Audrey Hepburn in \"Charade\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q8d173ea80a",
  "kind": "yes/no",
  "text": "Claim: Northeast Catholic College, is a non-profit, liberal arts, co-educational, four-year Catholic college founded in 1867 and located in Warner, a town in Merrimack County, New Hampshire, in the United States.\n\nPassages:\n\n[Northeast Catholic College]\nNortheast Catholic College (formerly The College of Saint Mary Magdalen) is a non-profit, liberal arts, co-educational, four-year Catholic college located in Warner, New Hampshire, United States.\n\n[Warner, New Hampshire]\nWarner is a town in Merrimack County, New Hampshire, United States.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q30f4cc1630",
  "kind": "yes/no",
  "text": "Post: Taxes  are just the best and I cannot wait to pay more 😇🥰🥺",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q6aff120489",
  "kind": "yes/no",
  "text": "Claim: Mock orange is a mostly Holarctic genus of shrubs. That genus contains more species than Sarracenia.\n\nPassages:\n\n[Sarracenia]\nSarracenia ( or ) is a genus comprising 8 to 11 species of North American pitcher plants, commonly called trumpet pitchers.\n\n[Philadelphus]\nPhiladelphus ( ) (mock-orange) is a genus of about 60 species of shrubs from 3-20 ft (1-6 m) tall, native to North America, Central America, Asia and (locally) in southeast Europe.\n\n[Mock orange]\nMock orange or mock-orange typically means \"Philadelphus\", a mostly Holarctic genus of shrubs, particularly the species \"Philadelphus coronarius\" which is widely cultivated as an ornamental.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q8dd04b76eb",
  "kind": "yes/no",
  "text": "Claim: The Lever Brothers parted with Margarine Unie to create an Indonesian soap factory.\n\nPassages:\n\n[Unilever Indonesia]\nPT Unilever Indonesia Tbk () was established in Indonesia on December 5, 1933 as Lever Zeepfabrieken N.V., a subsidiary of Lever Brothers which initially operated a soap factory at Angke, Jakarta.\n\n[Lever Brothers]\nIn 1930, Lever Brothers merged with Margarine Unie to form Unilever.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qede5f066e9",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which text is sarcastic?",
  "options": [
   "The healthcare system in the U.S is so frustrating. I spend so much money on health insurance only to end up paying just as much out of pocket when my insurance doesn’t cover the services.",
   "I love health insurance so much fun paying $100’s a month and then $100’s for basic medical services that somehow aren’t covered. #America"
  ]
 },
 {
  "qid": "qd6a3343a24",
  "kind": "yes/no",
  "text": "Text: considering crowd surfing the next time the hallways are too packed",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q1ff2197d39",
  "kind": "yes/no",
  "text": "Claim: The 1988 documentary film by Sandi Sissel was released before The End of Suburbia.\n\nPassages:\n\n[Sandi Sissel]\n\", \"Chicken Ranch\", \"Mother Teresa (1986)\" as well as TV shows like 60 Minutes, and feature films like \"Mr. and Mrs. Smith\".\n\n[The End of Suburbia]\nThe End of Suburbia: Oil Depletion and the Collapse of The American Dream is a 2004 documentary film concerning peak oil and its implications for the suburban lifestyle, written and directed by Toronto-based filmmaker Gregory Greene.\n\n[Chicken Ranch (film)]\nChicken Ranch is a 1983 documentary film by Nick Broomfield about the famous legalised brothel, the Chicken Ranch, in Pahrump, Nevada.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q681df990f4",
  "kind": "yes/no",
  "text": "Claim: A group formed by JYP Entertainment and debuted as a part of a seven member group whose first EP peak at number one on the \"Billboards\" World Albums Chart. This group produced the record \"Verse 2\".\n\nPassages:\n\n[JJ Project]\nJJ Project (Korean: 제이제이 프로젝트 ) is a South Korean pop duo, consisting of JB and Jinyoung. They were formed by JYP Entertainment and released their first single \"Bounce\" in May 2012.\n\n[Verse 2]\nVerse 2 is the first extended play by South Korean male duo JJ Project.\n\n[Got7]\nGot7 () is a South Korean boy group formed by JYP Entertainment. The group is composed of seven members: JB, Mark, Jackson, Jinyoung, Youngjae, BamBam, and Yugyeom. Got7 debuted in January 2014 with the release of their first EP \"Got It? \", which peaked at number two on the Gaon Album Chart and number one on \"Billboard's\" World Albums Chart.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 }
]
