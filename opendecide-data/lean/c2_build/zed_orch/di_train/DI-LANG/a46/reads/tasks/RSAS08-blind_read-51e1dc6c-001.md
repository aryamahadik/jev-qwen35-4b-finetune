# A46 replay label-noise blind read RSAS08-blind_read-51e1dc6c-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS08-blind_read-51e1dc6c-001.json

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
  "qid": "q787fa55c46",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "@JasperSmiith @LentonDNRA @ShearerWest @registrarism @UniofNottingham @CllrDaveTrimble @SallyLongford @CllrDavidMellen @LilianGreenwood @MyLWE @MyNottingham Yeah just a coincidence that infection rates go up and down dependent on when students are in the area or not, also tallies in with the parties being attended by up to 3 times the amount of allowed attendees. Definitely not students 🤔🤦🏽‍♀️🙄",
   "Yes there is a link and students are to blame for the rise in covid cases in our area."
  ]
 },
 {
  "qid": "qb20ebe6dcb",
  "kind": "yes/no",
  "text": "Claim: Of singers Kenny Greene and Billy Idol Kenny Greene is younger.\n\nPassages:\n\n[Kenny Greene]\nKenny Greene (January 17, 1969 – October 1, 2001) was an American singer-songwriter who was also a member of the R&B group Intro.\n\n[Billy Idol]\nWilliam Michael Albert Broad (born 30 November 1955), known professionally as Billy Idol, is an English musician, singer, songwriter, and actor.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q0fc3eb43bd",
  "kind": "yes/no",
  "text": "Claim: The city where the Róisín Dubh is located is in the Western area of a country. It is also the home of Sean Smyth. Mary Colum is from the country.\n\nPassages:\n\n[Galway]\nGalway ( ; Irish: \"Gaillimh\" , ] ) is a city in the West of Ireland in the province of Connacht.\n\n[Róisín Dubh (music venue)]\nThe Róisín Dubh is an established live music venue in Galway, Ireland.\n\n[Mary Colum]\nMary Colum (née Maguire, June 14, 1884 – October 22, 1957) was an Irish literary critic and author, who also co-founded a literary journal.\n\n[Seán Smyth]\nBorn in Straide, County Mayo, and now living in Galway, Seán is an All-Ireland champion on both fiddle and whistle .",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q629061dee8",
  "kind": "yes/no",
  "text": "Claim: The Japanese animator and film director Satoshi Kon was credited as \"Yoshihiro Wanibuchi,\" and directed the 2006 movie Paprika.\n\nPassages:\n\n[Satoshi Kon]\nSatoshi Kon (今 敏 , Kon Satoshi , October 12, 1963 – August 24, 2010) was a Japanese film director, animator, screenwriter and manga artist from Sapporo, Hokkaidō and a member of the Japanese Animation Creators Association (JAniCA). He is sometimes credited as \"Yoshihiro Wanibuchi\" (鰐淵良宏 , Wanibuchi Yoshihiro ) in the credits of \"Paranoia Agent\".\n\n[Paprika (2006 film)]\nPaprika (Japanese: パプリカ , Hepburn: Papurika ) is a 2006 Japanese science-fiction anime film co-written and directed by Satoshi Kon, based on Yasutaka Tsutsui's 1993 novel of the same name, about a research psychologist who uses a device that permits therapists to help patients by entering their dreams.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q5a29574ec3",
  "kind": "yes/no",
  "text": "Claim: Madrugada's final concert became popular one year after the band vocalist Kujibiki Unbalance, who is a member of MonstrO (band), sang with.\n\nPassages:\n\n[MonstrO (band)]\nMonstrO is an alternative band composed of former Still Rain, Danzig and Bloodsimple drummer Bevan Davies, former Bloodsimple, Medication and Skrew bassist Kyle Sanders, former Torche guitarist Juan Montoya and guitarist and vocalist Charlie Suarez formerly of Sunday Driver.\n\n[Madrugada (band)]\nOn 21 January 2008, the band released \"Madrugada\" and announced that they would split after one last tour. They performed their final concert on 15 November 2008.\n\n[Sunday Driver (band)]\nIn 2009 they became popular within the UK Steampunk scene.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q4d09436821",
  "kind": "yes/no",
  "text": "Claim: A driver won the Nation's Cup with Petter Solberg in Bushy Park, Barbados by two laps. He also won the 24 Hours of Le Mans nine times.\n\nPassages:\n\n[2014 Race of Champions]\nThe Nations' Cup was won by the Nordic team of Tom Kristensen and Petter Solberg, while the individual contest was won by David Coulthard, who beat Pascal Wehrlein 2–0 in the final.\n\n[Bushy Park, Barbados]\nLater in the same year it hosted the 2014 Race of Champions.\n\n[Tom Kristensen (racing driver)]\nHe holds the record for the most wins at the 24 Hours of Le Mans with nine, six of which were consecutive (from 2000 to 2005).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qeeeb33e5e4",
  "kind": "yes/no",
  "text": "Claim: The largest known example of European Iron Age bronze work is from Switzerland.\n\nPassages:\n\n[La Tène culture]\nThe La Tène culture ( ; ] ) was a European Iron Age culture named after the archaeological site of La Tène on the north side of Lake Neuchâtel in Switzerland, where thousands of objects had been deposited in the lake, as was discovered after the water level dropped in 1857.\n\n[Gundestrup cauldron]\nThe cauldron is the largest known example of European Iron Age silver work (diameter: 69 cm ; height: 42 cm ).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qe25eb1723a",
  "kind": "yes/no",
  "text": "Post: Day 38 of quarantine is an interesting time to get a new drum kit, neighbor",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qedd0d9dbbd",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Proper embarrassing that I was stopped by Tesco security. Hate my life.",
   "getting stopped by tesco security is the highlight of my day"
  ]
 },
 {
  "qid": "q810bcf6c5a",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "Kepa had a great game",
   "Kepa was sh*t"
  ]
 },
 {
  "qid": "q885ba95840",
  "kind": "yes/no",
  "text": "Claim: The former football goal keeper that was in the reality show De Pfaffs is older than Anne Noe.\n\nPassages:\n\n[Jean-Marie Pfaff]\nJean-Marie Pfaff (born 4 December 1953 in Lebbeke) is a Belgian former football goalkeeper who spent most of his professional career with Beveren and Bayern Munich.\n\n[De Pfaffs]\nDe Pfaffs was a Flemish reality show revolving around the family of former football goalkeeper Jean-Marie Pfaff.\n\n[Anne Noë]\nAnnie Ida Jenny Noë Haesendonck (born 13 April 1959) is a Belgian football coach and former international goalkeeper.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q8035383063",
  "kind": "yes/no",
  "text": "Claim: An actor stared in his first leading film role in 2015 in a film which was set in the Gangnam district of Seoul. This actor also appeared in The Legend of the Blue Sea.\n\nPassages:\n\n[Gangnam Blues]\nThe film is set in the 1970s against the backdrop of the real estate development of Seoul's Gangnam district amidst socio-political turmoil and terrorism.\n\n[Lee Min-ho (actor, born 1987)]\nLee starred in his first leading role in film with \"Gangnam Blues\" (2015), followed by his first China-produced film \"Bounty Hunters\" (2016).\n\n[The Legend of the Blue Sea]\nThe Legend of the Blue Sea () is a 2016-2017 South Korean television series starring Jun Ji-hyun and Lee Min-ho.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q937e7d5e94",
  "kind": "yes/no",
  "text": "Claim: A cocktail served in a Hurricane drinking glass and Fish House Punch both contain alcohol.\n\nPassages:\n\n[Hurricane glass]\nOther drinks served in this glass include the Singapore Sling, June bug, Piña colada and Blue Hawaii.\n\n[Fish House Punch]\nFish House Punch is a strong, rum-based punch containing rum, cognac, and peach brandy.\n\n[Singapore Sling]\nThe Singapore Sling is a gin-based cocktail from Singapore.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q21b5c21b69",
  "kind": "yes/no",
  "text": "Tweet: Need a new job 🙄",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qe7f68dd37a",
  "kind": "yes/no",
  "text": "Claim: Sophia Grace & Rosie featured a cover song on their Youtube channel. The song from is from an album released under the Syco Music and Columbia Records labels.\n\nPassages:\n\n[Sophia Grace &amp; Rosie]\nRosie has started a YouTube channel featuring her life and sang a cover of Little Mix's \"Touch\".\n\n[Touch (Little Mix song)]\n\"Touch\" is a song by British girl group Little Mix. It was released as the second single from their studio album \"Glory Days\".\n\n[Glory Days (Little Mix album)]\nIt was released on 18 November 2016, by Syco Music and Columbia Records.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q2e1985f26a",
  "kind": "yes/no",
  "text": "Claim: seven novels are in the C.S. Lewis series that a Kosovoian series has been compared to. O Saci (film) was the first theatrical adaptation of this series from Kosovo .\n\nPassages:\n\n[Sítio do Picapau Amarelo (novel series)]\nThe series is considered representative of Brazilian children's literature and as the Brazilian equivalent to children's classics such as C. S. Lewis, \"The Chronicles of Narnia\" and L. Frank Baum's \"The Wonderful Wizard of Oz\" series.\n\n[O Saci (film)]\nNoted for being the first family film to be ever made in Brazil, it is also the first theatrical \"Sítio do Picapau Amarelo\" adaptation.\n\n[The Chronicles of Narnia]\nThe Chronicles of Narnia is a series of seven fantasy novels by C. S. Lewis.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qd491742177",
  "kind": "yes/no",
  "text": "Claim: The Emerald Wand of Oz was published by the comapny that is headquartered in New York City.\n\nPassages:\n\n[The Emerald Wand of Oz]\nThe book is illustrated by William Stout and published by Harper Collins.\n\n[HarperCollins]\nThe company is headquartered in New York City and is a subsidiary of News Corp.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q1cb1d79d8e",
  "kind": "yes/no",
  "text": "Claim: The comedy play written by Shakespeare in 1604 which inspired the movie \"She's the Man\", is also know by the name What You Will.\n\nPassages:\n\n[She's the Man]\nInspired by William Shakespeare's play \"Twelfth Night\", it is a remake of the 1985 film \"Just One of the Guys\".\n\n[Twelfth Night]\nTwelfth Night, or What You Will is a comedy by William Shakespeare, believed to have been written around 1601–02 as a Twelfth Night's entertainment for the close of the Christmas season.\n\n[Chiltern Shakespeare Company]\nRecent productions include \"Much Ado about Nothing\", \"Twelfth Night\", \"A Midsummer Night's Dream\", \"As You Like It\", \"The Taming of the Shrew\", \"The Merchant of Venice\" and \"The Merry Wives of Windsor\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qbac6c6ecca",
  "kind": "yes/no",
  "text": "Claim: Evil controllers was featured on Game informer who was published by the monthly video magazine corporation GameStop Corp.\n\nPassages:\n\n[Evil Controllers]\nEvil Controllers has been featured on majoring gaming sites such as IGN, Kotaku and Game Informer for their Controller Creator that allows shoppers to make fully custom controllers.\n\n[Game Informer]\nThe publication is owned and published by GameStop Corp., the parent company of the video game retailer of the same name, who bought FuncoLand in 2000.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qd45385684b",
  "kind": "yes/no",
  "text": "Tweet: 10 things i hate about you is the best movie of all time",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q5133cd175c",
  "kind": "yes/no",
  "text": "Claim: I Get Off is the first single from the rock band. This band and \"Say Anything\" are from different states.\n\nPassages:\n\n[I Get Off]\n\"I Get Off\" is the first single released by the hard rock band, Halestorm.\n\n[Halestorm]\nHalestorm is an American hard rock band from Red Lion, Pennsylvania, consisting of lead vocalist and guitarist Lzzy Hale, her brother drummer and percussionist Arejay Hale, guitarist Joe Hottinger, and bassist Josh Smith.\n\n[Say Anything (band)]\nSay Anything is an American rock band from Los Angeles, California.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q486b5d0148",
  "kind": "yes/no",
  "text": "Claim: Ulrich of Eppenstein served as an abbot for an Abbey located in the city of St. Gallen in Switzerland.\n\nPassages:\n\n[Ulrich of Eppenstein]\nca.1047–1121) served between 1071 and his death as Abbot of the powerful Abbey of Saint Gall.\n\n[Abbey of Saint Gall]\nThe Abbey of Saint Gall (German: Abtei St. Gallen ) is a dissolved abbey (747–1805) in a Roman Catholic religious complex in the city of St. Gallen in Switzerland.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qe1d83dd56e",
  "kind": "yes/no",
  "text": "Claim: Rennae Stubs who teamed up with Elena Bovina for the 2003 Family Circle Cup – Doubles. Her and Renáta Tomanová were both tennis players\n\nPassages:\n\n[Renáta Tomanová]\nRenáta Tomanová (born 9 December 1954) is a former professional tennis player from Czechoslovakia.\n\n[2003 Family Circle Cup – Doubles]\nLisa Raymond and Rennae Stubbs were the defending champions, but Raymond did not compete in this edition.\n\n[Rennae Stubbs]\nRennae Stubbs (born 26 March 1971) is an Australian retired tennis player.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe007ed3f8e",
  "kind": "yes/no",
  "text": "Claim: The actress who starred in the online movie was in the 2009 cop show that aired on the network KBS2. The online movie was directed by Lee Jae-kyoo.\n\nPassages:\n\n[Boys Over Flowers (TV series)]\nIt aired on KBS2 from January 5 to March 31, 2009 on Mondays and Tuesdays at 22:00 for 25 episodes.\n\n[Lee Jae-kyoo]\nLee directed the television series \"Damo\" (2003), \"Fashion 70's\" (2005), \"Beethoven Virus\" (2008), and \"The King 2 Hearts\" (2012), as well as the online movie \"The Influence\" (2010) and \"The Fatal Encounter\" (2014).\n\n[The Influence (film)]\nThe Influence () is a four-part online film starring Lee Byung-hun and Han Chae-young.\n\n[Han Chae-young]\nShe is known for her notable roles in several Korean dramas such as \"Autumn in My Heart\", \"Delightful Girl Choon-Hyang\", \"Only You\", \"Fireworks\", \"Boys Over Flowers\", \"A Man Called God\" and \"Pretty Man\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q07ac57039d",
  "kind": "yes/no",
  "text": "Tweet: Queer marriage is not allowed because it doesn't follow the \"age-old customs, rituals, practices, culturla ethos and societal values\", but all cis-men can commit infidelity with no consequences. Happy fuckin Pride people 🙃 #SupremeCourtofIndia",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qdd2ea5ffe9",
  "kind": "yes/no",
  "text": "Claim: Russia Soviet pianist, composer and teacher, Tatiana Nikolayeva taught Russian pianist and music educator Maria Szraiber.\n\nPassages:\n\n[Tatiana Nikolayeva]\nTatyana Petrovna Nikolayeva (Russian: Татья́на Петро́вна Никола́ева , \"Tat'jana Petrovna Nikolaeva\"; May 4, 1924November 22, 1993) was a Russian Soviet pianist, composer and teacher.\n\n[Maria Szraiber]\nMaria Szraiber is a Polish pianist and music educator.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qf616f08958",
  "kind": "yes/no",
  "text": "Claim: The band Steve Goulding is the drummer for is not British. The singer whose debut album is Don't Let It Go to Waste isn't British either.\n\nPassages:\n\n[Don't Let It Go to Waste]\nDon't Let It Go to Waste is the debut album from Matt Willis, released on 20 November 2006.\n\n[The Mekons]\nThe Mekons are a British-American rock band.\n\n[Steve Goulding]\nSteve Goulding (born 1954, South London, England) is an English drummer, who has played as a member of Graham Parker and The Rumour, The Associates, Poi Dog Pondering, The Waco Brothers and The Mekons.\n\n[Matt Willis]\nMathew James \"Matt\" Willis (born 8 May 1983), also previously known as Mattie Jay, is an English singer-songwriter, television presenter and actor, best known as the bassist and one of the vocalists of the pop punk band, Busted.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q84a71fa97c",
  "kind": "yes/no",
  "text": "Claim: Nerdcore Rising and What Would Jesus Buy movies are not focused on similar topics.\n\nPassages:\n\n[What Would Jesus Buy?]\nWhat Would Jesus Buy? is a 2007 documentary film produced by Morgan Spurlock and directed by Rob VanAlkemade. The title is a take-off on the phrase \"What would Jesus do?\n\n[Nerdcore Rising (film)]\nNerdcore Rising is a documentary/concert film starring MC Frontalot and other nerdcore hip hop artists such as mc chris, Wheelie Cyberman of Optimus Rhyme and MC Lars, with contributors from artists such as \"Weird Al\" Yankovic, Prince Paul, and Brian Posehn.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa1f3b78ca8",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "The ending to Pay It Forward made me extremely sad and I’m not happy about it.",
   "pay it forward is honestly one of the worst movies I've ever seen why would would anyone make an ending so sad I've been crying for 30 min"
  ]
 },
 {
  "qid": "qd83977557e",
  "kind": "yes/no",
  "text": "Claim: \"Licence Revoked\" was the original title during production of a film that has the leading actor from another film. The actor stars as villain Franz Sanchez in \"Licence Revoked\". The actor stars as villain Franz Sanchez in \"Licence Revoked\". Laurene Landon starred in the other role.\n\nPassages:\n\n[Laurene Landon]\nShe is best known for her roles in \"Maniac Cop\" and \"Maniac Cop 2\", \"Hundra\", \"\", and \"...All the Marbles\" with Peter Falk.\n\n[Licence to Kill]\nOriginally titled \"Licence Revoked\" in line with the plot, the name was changed during post-production due to test audiences associating the term with driving.\n\n[Robert Davi]\nAmong his most recognized roles are opera-singing heavy Jake Fratelli in \"The Goonies\" (1985), Vietnam veteran and FBI Special Agent Big Johnson in \"Die Hard\" (1988), Bond villain Franz Sanchez in \"Licence to Kill\" (1989), police deputy chief Phil Heinemann in \"Predator 2\" (1990), strip club manager Al Torres in \"Showgirls\" (1995) and Albanian mob boss Goran Vata in \"The Expendables 3\" (2014).\n\n[Maniac Cop 2]\nit stars Robert Davi, Claudia Christian, Michael Lerner, and Bruce Campbell.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa71888d854",
  "kind": "yes/no",
  "text": "Claim: American singer Aaliyah had a video director that directed the music video Soothe My Soul, and also had to face allegation of illegal marriage with Aaliyah Dana Haughton.\n\nPassages:\n\n[Soothe My Soul]\nThe music video directed by Warren Fu was premiered on 28 March 2013.\n\n[Warren Fu]\nHe has directed promos for Daft Punk, The Weeknd, Snoop Dogg, Pharrell Williams, The Strokes, HAIM, The Killers, Depeche Mode, Weezer, Mark Ronson, Julian Casablancas, and Aaliyah.\n\n[Aaliyah]\nAfter facing allegations of an illegal marriage with R. Kelly, Aaliyah ended her contract with Jive and signed with Atlantic Records.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb529502b26",
  "kind": "yes/no",
  "text": "Claim: Julia Smith and Tony Holland were the creators of the long-running British soap opera in which Alison Pargeter plays the role of Sarah Cairns.\n\nPassages:\n\n[EastEnders]\nEastEnders is a long-running British soap opera created by Julia Smith and Tony Holland which has been broadcast on BBC One since 1985.\n\n[Alison Pargeter]\nAlison Pargeter (born 31 May 1972) is an English actress who played the roles of stalker Sarah Cairns in the BBC soap opera \"EastEnders\", also Mary Slessor in an 11-part television series of\" Mary Slessor\", and the Nag's Head barmaid called Val in the BBC \"Only Fools and Horses\" prequel \"Rock & Chips\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7e52b08635",
  "kind": "yes/no",
  "text": "Claim: Many jack-in-the-boxes use an English nursery rhyme with a Roud Folk Song Index score of 5249.\n\nPassages:\n\n[Pop Goes the Weasel]\nIt has a Roud Folk Song Index number of 5249.\n\n[Jack-in-the-box]\nMany which use \"Pop Goes the Weasel\" open at the point in the melody where the word \"pop\" would be if it were sung.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qd7d522bc6e",
  "kind": "yes/no",
  "text": "Post: Guys literally confuse the SHIT out of me",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q03f32933e8",
  "kind": "yes/no",
  "text": "Claim: The Gujarat Lions are captained by this Sri-Lankan woman. She is the second youngest cricket captain to play in the 2016 Indian Premier League.\n\nPassages:\n\n[Suresh Raina]\nHe has also captained the Indian cricket team and is the second-youngest player ever to captain India.\n\n[Gujarat Lions in 2017]\nThey are captained by Suresh Raina and coached by Brad Hodge.\n\n[Gujarat Lions in 2016]\nThey are one of the eight teams competing in the 2016 Indian Premier League. They are captained by Suresh Raina and coached by Brad Hodge.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc11277b62b",
  "kind": "yes/no",
  "text": "Claim: Prince Royce directed the movie for which Jason O'Bryan was nominated for a grammy for best soundtrack.\n\nPassages:\n\n[Jason O'Bryan]\nHe was a member of the Dub Pistols (1997–2010) and worked on the Grammy Award nominated soundtrack of the film \"Y Tu Mamá También\".\n\n[Y Tu Mamá También]\nY Tu Mamá También (English: \"And Your Mother Too\" ) is a 2001 Mexican drama film directed by Alfonso Cuarón and co-written by Cuarón and his brother Carlos.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qf54022bc0f",
  "kind": "yes/no",
  "text": "Claim: The Italian coach of the team, that won the 2008 Texas vs. Texas Tech football game , was born March 9, 1961.\n\nPassages:\n\n[2008 Texas Tech Red Raiders football team]\nThe team was coached by Mike Leach.\n\n[2008 Texas vs. Texas Tech football game]\nThe 2008 Texas vs. Texas Tech football game was a Big 12 Conference game played between the Texas Longhorns and Texas Tech Red Raiders at Jones AT&T Stadium in Lubbock, Texas, United States.\n\n[Mike Leach (American football coach)]\nMichael Charles Leach (born March 9, 1961) is an American college football coach.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q0f5a744b90",
  "kind": "yes/no",
  "text": "Claim: The 500 ft McCarthy Building was added to the National Register of Historic Places at the same time as the oldest building on Monument Square.\n\nPassages:\n\n[McCarthy Building (Troy, New York)]\nThe McCarthy Building is located on River Street on the west side of Monument Square in Troy, New York, United States. In 1970 it was added to the National Register of Historic Places in 1970, along with the nearby Cannon Building.\n\n[Cannon Building (Troy, New York)]\nIt is the oldest building on Monument Square. In 1970 it was listed on the National Register of Historic Places.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q785564ac72",
  "kind": "yes/no",
  "text": "Claim: Trade unions were legalized in Tony Blair's country in 1871.\n\nPassages:\n\n[Trade unions in the United Kingdom]\nLegalised in 1871, the trade union movement sought to reform socio-economic conditions for working men in British industries, and the trade unions' search for this led to the creation of a Labour Representation Committee which effectively formed the basis for today's Labour Party, which still has extensive links with the Trade Union Movement in Britain.\n\n[Tony Blair]\nAnthony Charles Lynton Blair (born 6 May 1953) is a British politician who served as Prime Minister of the United Kingdom from 2 May 1997 to 27 June 2007 and Leader of the Labour Party from 21 July 1994 to 24 June 2007.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q987d0f41c8",
  "kind": "yes/no",
  "text": "Claim: John Updike and Tom Clancy both publish more than 15 bestselling novels.\n\nPassages:\n\n[Tom Clancy]\nSeventeen of his novels were bestsellers, and more than 100 million copies of his books are in print.\n\n[John Updike]\nOne of only three writers to win the Pulitzer Prize for Fiction more than once (the others were Booth Tarkington and William Faulkner), Updike published more than twenty novels, more than a dozen short-story collections, as well as poetry, art and literary criticism and children's books during his career.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qba6ff14b96",
  "kind": "yes/no",
  "text": "Claim: Sangerville Town Hall is located at 1 Town Hall Lane (corner of South Main Street) in the village center of Sangerville, Maine, Sangerville is a town in Piscataquis County, Maine, in the United States.\n\nPassages:\n\n[Sangerville, Maine]\nSangerville is a town in Piscataquis County, Maine, United States.\n\n[Sangerville Town Hall]\nSangerville Town Hall is located at 1 Town Hall Lane (corner of South Main Street) in the village center of Sangerville, Maine.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc14395ceb2",
  "kind": "yes/no",
  "text": "Post: Pernille deserves better",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qb67691e688",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "Ratings should not matter.",
   "@SuspendThePres But what were the ratings?? (Replied to his Tweet with the same thing.)"
  ]
 },
 {
  "qid": "q247a5f83d1",
  "kind": "yes/no",
  "text": "Claim: Christopher Michael \"Chris\" DeStefano has written more top songs than this American country music artist, who co-wrote and recorded Drunk on Your Love.\n\nPassages:\n\n[Brett Eldredge]\nThe cousin of Terry Eldredge of The Grascals, Eldredge has had three No. 1 singles on the \"Billboard\" Country Airplay chart from his debut studio album, \"Bring You Back\": \"Don't Ya\", \"Beat of the Music\", and \"Mean to Me\".\n\n[Chris DeStefano]\nChristopher Michael \"Chris\" DeStefano is a Grammy Award Winning American singer/songwriter, record producer and multi instrumentalist, raised in Mt. Laurel, New Jersey and currently residing in Nashville, Tennessee. As a songwriter, he has multiple #1 songs with artists Carrie Underwood (“Good Girl”, \"Little Toy Guns\"), Billy Currington (“Hey Girl”), Brett Eldredge (\"Don't Ya\"), Luke Bryan (\"That's My Kind of Night\", \"Kick the Dust Up\" ), Miranda Lambert & Carrie Underwood (\"Somethin' Bad,\" later reworked as the opening theme for \"NBC Sunday Night Football\"), Rascal Flatts (\"Rewind\") and Jason Aldean (\"Just Gettin' Started\").\n\n[Drunk on Your Love]\n\"Drunk on Your Love\" is a song co-written and recorded by American country music artist Brett Eldredge.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qdca35552ce",
  "kind": "yes/no",
  "text": "Claim: Trouble Every Day is the name of both the Tindersticks' soundtrack and a film written by Denis and Jean-Pol Fargeau both released in 1983.\n\nPassages:\n\n[Trouble Every Day (soundtrack)]\nTrouble Every Day is the name of Tindersticks' soundtrack to French director Claire Denis's 2001 film \"Trouble Every Day\".\n\n[Trouble Every Day (film)]\nTrouble Every Day is a 2001 French erotic horror film directed by Claire Denis and written by Denis and Jean-Pol Fargeau.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q57c2a7349a",
  "kind": "yes/no",
  "text": "Claim: The most important surviving 16th century Byzantine building in Ayakapı and an area in the Faith district are both located in Istanbul, Turkey. This area is also home to the Turkish and Islamic Arts Museum.\n\nPassages:\n\n[Ayakapı]\nIn Ayakapı lies one of the most important surviving Byzantine buildings of the historical peninsula, the Gül Mosque.\n\n[Turkish and Islamic Arts Museum]\nThe Turkish and Islamic Arts Museum (Turkish: \"\" ) is a museum located in Sultanahmet Square in Fatih district of Istanbul, Turkey.\n\n[Gül Mosque]\nGül Mosque (Turkish: \"Gül Camii\" , meaning: \"The Mosque of the Rose\" in English) is a former Eastern Orthodox church in Istanbul, Turkey, converted into a mosque by the Ottomans.\n\n[Hippodrome of Constantinople]\nToday it is a square named \"Sultanahmet Meydanı\" (\"Sultan Ahmet Square\") in the Turkish city of Istanbul, with a few fragments of the original structure surviving.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q39d2cddc9b",
  "kind": "yes/no",
  "text": "Claim: Chantal Claret is a singer. So is the writer of the song \"I'm Just a Kid\".\n\nPassages:\n\n[Chantal Claret]\nShe is best known as the lead singer for the rock and power pop band Morningwood.\n\n[I'm Just a Kid]\n\"I'm Just a Kid\" is the debut single by the band Simple Plan, written by Pierre Bouvier.\n\n[Pierre Bouvier]\nPierre Charles Bouvier {'1': \", '2': \", '3': \", '4': \"} (born 9 May 1979) is a Canadian singer, songwriter, musician, composer and actor who is best known as the lead singer and guitarist of the rock band Simple Plan.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qcbb553fa6a",
  "kind": "yes/no",
  "text": "Claim: The film that Pocahontas II: Journey to a New World was a sequel to, Pocahontas (1995 film), was made before Born in China which was released in 1991.\n\nPassages:\n\n[Pocahontas (1995 film)]\nPocahontas is a 1995 American animated musical romantic-comedy-drama film produced by Walt Disney Feature Animation for Walt Disney Pictures.\n\n[Pocahontas II: Journey to a New World]\nPocahontas II: Journey to a New World is a 1998 straight-to-video sequel to the 1995 Disney film \"Pocahontas\".\n\n[Born in China]\nBorn in China (我們誕生在中國) is a 2016 nature documentary film directed by Lu Chuan.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q0e1d1d88bd",
  "kind": "yes/no",
  "text": "Claim: South America is the region that does not have the indigenous language that includes the word which is the common name of a species of plant called \"Erythroxylum vacciniifolium \".\n\nPassages:\n\n[Erythroxylum]\nAnother species, \"Erythroxylum vacciniifolium\" (also known as Catuaba) is used as an aphrodisiac in Brazilian drinks and herbal medicine.\n\n[Catuaba]\n'aba], a Guarani word that means \"what gives strength to the Indian\") is used for the infusions of the bark of a number of trees native to Brazil.\n\n[Guarani language]\nGuarani ( or ), specifically the primary variety known as Paraguayan Guarani (endonym \"avañe'ẽ\" ] 'the people's language'), is an indigenous language of South America that belongs to the Tupi–Guarani family of the Tupian languages.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qcba00889b0",
  "kind": "yes/no",
  "text": "Claim: Dennis Potter wrote the TV serial in which Rosemary Martin played Marjorie.\n\nPassages:\n\n[Pennies from Heaven (TV series)]\nPennies From Heaven is a 1978 BBC musical drama serial written by Dennis Potter.\n\n[Rosemary Martin]\n\", Marjorie in \"Pennies from Heaven\", Miss Weber in \"The Insurance Man\", Renie Fox in \"Fox\" and Verna Johnson in \"Tenko\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 }
]
