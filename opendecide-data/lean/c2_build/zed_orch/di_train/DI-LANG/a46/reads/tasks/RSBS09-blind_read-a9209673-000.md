# A46 replay label-noise blind read RSBS09-blind_read-a9209673-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS09-blind_read-a9209673-000.json

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
  "qid": "q684d912945",
  "kind": "yes/no",
  "text": "Claim: The magazine owned by Sarah Magoo for which James P. Comer has written more than 150 articles, and Madame Figaro are not published in the same country.\n\nPassages:\n\n[James P. Comer]\nHe has also written more than 150 articles for Parents (magazine) and more than 300 articles on children's health and development and race relations.\n\n[Parents (magazine)]\nParents, published by Meredith Corporation, is an American mass circulation monthly magazine that features scientific information on child development geared to help parents in raising their children.\n\n[Madame Figaro]\nMadame Figaro is a French magazine supplement to the Saturday edition of the daily newspaper \"Le Figaro\", focusing on and catering to women.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3c7f78cdee",
  "kind": "yes/no",
  "text": "Claim: The head coach of the 1985 Oklahoma Sooners led the Dallas Cowboys to a Super Bowl victory in 1982.\n\nPassages:\n\n[Barry Switzer]\nHe served for 16 years as head football coach at the University of Oklahoma and four years as head coach for the Dallas Cowboys of the National Football League (NFL). He helped the Cowboys win Super Bowl XXX against the Pittsburgh Steelers.\n\n[1985 NCAA Division I-A football season]\nThe 1985 NCAA Division I-A football season saw the Oklahoma Sooners, led by head coach Barry Switzer, win the national championship.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q10266eb5ca",
  "kind": "yes/no",
  "text": "Text: So, very delayed flight from Bristol to Edinburgh @easyJet, trademark vagueness from staff, with a chronic lack of empathy to boot (despite me travelling with three young children)... now, time to feed our family with £3 vouchers (at airport prices!) #bollocks",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q333de9ff4d",
  "kind": "yes/no",
  "text": "Claim: Beside the American university administrator and politician from the state of Oklahoma, David McCurdy was part of the Boren-McCurdy proposals.\n\nPassages:\n\n[David L. Boren]\nDavid Lyle Boren (born April 21, 1941) is an American university administrator and politician from the state of Oklahoma.\n\n[Boren-McCurdy proposals]\nThe Boren-McCurdy intelligence reform proposals are two legislative proposals from Senator David Boren and Representative David McCurdy in 1992 (102nd Congress).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qc67c9b1c1d",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "every time i send my mom pictures of me and one of my friends doing fun things the first question she asks is if we're on a date what are you trying to tell me mother",
   "my mom thinks i'm dating every one of my friends whenever i send her pictures because she thinks i'm lonely."
  ]
 },
 {
  "qid": "q88c7ad5ef7",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Billy Gunn is actually in the spotlight now.",
   "Billy Gunn sorta relevant for the first time in years..."
  ]
 },
 {
  "qid": "q967e039900",
  "kind": "yes/no",
  "text": "Tweet: love it when Jonny makes me use earphones to watch something on my phone so he can play fifa",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qa06d38494c",
  "kind": "yes/no",
  "text": "Claim: The Polar Bear and Daiquiri drinks are not cocktails.\n\nPassages:\n\n[Daiquiri]\nDaiquiri ( ; Spanish: \"daiquirí\" ] ) is a family of cocktails whose main ingredients are rum, citrus juice (typically lime juice), and sugar or other sweetener.\n\n[Polar Bear (cocktail)]\nA Polar Bear, After Eight or Peppermint Paddy (a play on \"Peppermint Pattie\") is a mint chocolate cocktail that tastes like a York Peppermint Pattie or an After Eight wafer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q8aa6ee08ce",
  "kind": "yes/no",
  "text": "Claim: Broken Bridges is a 2006 film that starred an American actress who appeared in Twins and Jerry Maguire, and is married to John Travolta.\n\nPassages:\n\n[Broken Bridges]\nBroken Bridges is a 2006 film starring Toby Keith, Lindsey Haun, Burt Reynolds and Kelly Preston.\n\n[Kelly Preston]\nKelly Preston (born October 13, 1962) is an American actress and former model. She has appeared in more than sixty television and film productions, most notably including \"Mischief\", \"Twins\" and \"Jerry Maguire\". She is married to John Travolta, with whom she collaborated on the fantasy film \"Battlefield Earth\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q2d261d7876",
  "kind": "yes/no",
  "text": "Claim: Nikita Gennadyevich Katsalapov won the 2016 Russian national silver medal with another Russian ice dancer born 29 April 1995.\n\nPassages:\n\n[Victoria Sinitsina]\nVictoria Alexandrovna Sinitsina (Russian: Виктория Александровна Синицина ; born 29 April 1995) is a Russian ice dancer.\n\n[Nikita Katsalapov]\nNikita Gennadyevich Katsalapov (Russian: Никита Геннадьевич Кацалапов ; born 10 July 1991) is a Russian ice dancer. With Victoria Sinitsina, he is the 2016 Russian national silver medalist.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q23ce9835b9",
  "kind": "yes/no",
  "text": "Claim: The composer, for the music in the film soundtrack reworked by this group, was born in Rhode Island. The name of this group is also the title of an album by the band that did Ancient Cross Dressing Songs.\n\nPassages:\n\n[Melora a la Basilica]\nIt is a collection of previous Rasputina songs reworked with new band member Daniel DeJesus and covers of songs by Goldfrapp, Pearl Jam and the Sweeney Todd and A Clockwork Orange soundtracks.\n\n[A Clockwork Orange (soundtrack)]\nThe soundtrack of \"A Clockwork Orange\" comprises classical music and electronic synthetic music composed by Wendy Carlos (then Walter Carlos).\n\n[Wendy Carlos]\nBorn and raised in Rhode Island, Carlos studied physics and music at Brown University before moving to New York City in 1962 to study music composition at Columbia University.\n\n[Ancient Cross-Dressing Songs]\nMuch like their two previous EPs, Melora a la Basilica and The Willow Tree Triptych, the album is available only via the band's website and is hand-crafted by Creager herself.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q253b831889",
  "kind": "yes/no",
  "text": "Claim: Xentrix had music videos for their cover of a pop song written and recorded by Ray Parker, Jr. That song is the theme song for a movie starring a Canadian-American actor who was an original member of the Not Ready for Prime Time Players on Saturday Night Live.\n\nPassages:\n\n[Dan Aykroyd]\nDaniel Edward Aykroyd {'1': \", '2': \", '3': \", '4': \"} (born July 1, 1952) is a Canadian-American actor, comedian, producer, screenwriter, musician and businessman. He was an original member of the \"Not Ready for Prime Time Players\" on \"Saturday Night Live\" (1975–1979).\n\n[Xentrix]\nThey had music videos for their cover of Ray Parker, Jr's \"Ghostbusters\" as well as the songs \"Crimes\", \"For Whose Advantage?\n\n[Ghostbusters (song)]\n\"Ghostbusters\" is a song written and recorded by Ray Parker Jr. as the theme to the film of the same name starring Bill Murray, Dan Aykroyd, Harold Ramis, and Ernie Hudson.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qef3b89a58e",
  "kind": "yes/no",
  "text": "Claim: The German artist who is credited with inventing the V-2 rocket and Saturn V was also a supervisor of the April 6, 1967-launched communication satellite NASA program.\n\nPassages:\n\n[Applications Technology Satellite]\nThe Applications Technology Satellites (ATS) were a series of experimental satellites launched by NASA, under the supervision of, among others, Wernher von Braun.\n\n[ATS-2]\nATS-2 (Applications Technology Satellite) was a communications satellite launched by NASA on April 6, 1967 on an Atlas-Agena D rocket from Cape Canaveral.\n\n[Wernher von Braun]\nWernher Magnus Maximilian Freiherr von Braun (March 23, 1912 – June 16, 1977) was a German, later American, aerospace engineer and space architect credited with inventing the V-2 rocket for Nazi Germany and the Saturn V for the United States.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qbbc9e4e61f",
  "kind": "yes/no",
  "text": "Claim: The Ruthe Balock Jones tribe is based in central Bartlesville, Oklahoma.\n\nPassages:\n\n[Ruthe Blalock Jones]\nRuthe Blalock Jones (born 1939) is a Delaware-Shawnee-Peoria painter and printmaker from Oklahoma.\n\n[Delaware Tribe of Indians]\nThe Delaware Tribe of Indians, sometimes called the Eastern Delaware, based in Bartlesville, Oklahoma, is one of three federally recognized tribes of Delaware Indians in the United States, along with the Delaware Nation based in Anadarko, Oklahoma and the Stockbridge-Munsee Community of Wisconsin.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q0eef43938e",
  "kind": "yes/no",
  "text": "Tweet: @tedcruz @Dream worst timeline",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q5ce591615e",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Legos are exhilarating",
   "High stakes legos"
  ]
 },
 {
  "qid": "q1d862f0cb1",
  "kind": "yes/no",
  "text": "Claim: Royler Gracie was a student of the person who also taught Romero Cavalcanti and ran the Gracie Humaitá school in Rio de Janeiro.\n\nPassages:\n\n[Royler Gracie]\nHe ran the Gracie Humaitá school in Rio de Janeiro, Brazil for many years under his father Helio's direction, but currently lives in San Diego.\n\n[Rodrigo Medeiros]\nHe received his black belt from Rolls Gracie student, Romero \"Jacaré\" Cavalcanti, he also trained under Fernando 'Magrao' Gurgel and is one of a select group of Jiu-Jitsu competitors to have won the prestigious World Jiu-Jitsu Championship openweight titles twice.\n\n[Rolls Gracie]\nRolls Gracie ([ˈɡɾejsi] 1951–1982) was a Brazilian martial artist. He was teacher of Rickson Gracie, Carlos Gracie Jr., Royler Gracie, Márcio \"Macarrão\" Stambowsky, Rigan Machado and Romero \"Jacare\" Cavalcanti.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q7e55fbae99",
  "kind": "yes/no",
  "text": "Claim: The song, which Billie Anthony is best known for her Top 10 hit version, topped the UK chart in 1981 in a recording by a platinum-selling Welsh rock and roll singer whose recording and performing career began in the late 1960s.\n\nPassages:\n\n[Shakin' Stevens]\nMichael Barratt (born 4 March 1948), known as Shakin' Stevens, is a platinum-selling British rock and roll singer and songwriter who was the UK's biggest-selling singles artist of the 1980s. His recording and performing career began in the late 1960s, although it was not until 1980 that his commercial success began.\n\n[Billie Anthony]\nShe is best known for her Top 10 hit version of \"This Ole House\", which despite chart competition from other versions of the same song, reached No. 4 in the UK chart.\n\n[This Ole House]\n\"This Ole House\" (sometimes written \"This Old House\") is a popular song written by Stuart Hamblen, and published in 1954. The song again topped the UK chart in 1981 in a recording by Shakin' Stevens.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q419a5e0afb",
  "kind": "yes/no",
  "text": "Claim: The actor and film director of the 1990s crime thriller, won his first Academy Award for The Usual Suspects. They have since collaborated with the director of the 2014 film \"The Guvnors\".\n\nPassages:\n\n[The Guvnors]\nThe Guvnors is a 2014 film directed by Gabe Turner.\n\n[Gabe Turner]\nHe has worked as a Producer, Director and Writer who regularly collaborates on TV and film projects featuring some of the worlds most recognised actors and sports stars including Meryl Streep, Arnold Schwarzenegger, David Beckham, James Corden, Billy Crystal and Kevin Spacey.\n\n[Kevin Spacey]\nHe gained critical acclaim in the early 1990s that culminated in his first Academy Award for Best Supporting Actor for the neo-noir crime thriller \"The Usual Suspects\" (1995), and an Academy Award for Best Actor for midlife crisis-themed drama \"American Beauty\" (1999).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qe66bf8ad6f",
  "kind": "yes/no",
  "text": "Claim: The author of Mystery is a novelist. So is the author of The Playmaker.\n\nPassages:\n\n[Mystery (novel)]\nMystery is a 1990 novel by American author Peter Straub, and is the second installment in Straub's loosely connected \"Blue Rose Trilogy\".\n\n[Thomas Keneally]\nThomas Michael Keneally, AO (born 7 October 1935) is a prolific Australian novelist, playwright, and essayist.\n\n[The Playmaker]\nThe Playmaker is a novel based in Australia written by the Australian author Thomas Keneally.\n\n[Peter Straub]\nPeter Francis Straub (born March 2, 1943) is an American novelist and poet.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qa3f2ed60a3",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which text is sarcastic?",
  "options": [
   "We decided to record on the evening of the 6th, which was unfortunate because at the same time some significant events were happening that we probably would have talked about.",
   "Ok, so @bytereview and I decided to record on the evening of the 6th, just as absolutely nothing newsworthy was happening! Perfect timing as always, to go over some of the best ITSBUPs of 2020 - and how we're settling into 2021! Listen: https://t.co/oaPLwrtcHP https://t.co/za3EHuqcWh"
  ]
 },
 {
  "qid": "qca1f53b60b",
  "kind": "yes/no",
  "text": "Claim: Griffon Bruxellois refers to more groups than an old established breed of rare breed dog does.\n\nPassages:\n\n[Rare breed (dog)]\nRare breed (dog) is any breed of dog that is small in number and is used to refer to both old established breeds such as the Stabyhoun and Glen of Imaal Terrier or newer creations.\n\n[Griffon Bruxellois]\nThe Griffon Bruxellois may refer to three different breeds, the Griffon Bruxellois, the Griffon Belge and the Petit Brabançon.\n\n[Stabyhoun]\nThe Stabyhoun or Stabij is one of the top five rarest dog breeds in the world.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q48a0930710",
  "kind": "yes/no",
  "text": "Text: mentally I’m hiding in the walk-in",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q504a366794",
  "kind": "yes/no",
  "text": "Claim: Strings, Ali Azmat, Shahzad Hasan and another woman are returning judges on the show Music Icons. The producer and singer of Aaina joined them. The other woman starred in Mor Mahal.\n\nPassages:\n\n[Ali Azmat]\nAli Azmat (born April 20, 1970) is a Pakistani singer-songwriter, musician and actor.\n\n[Alamgir (pop singer)]\nIn April 2013, Alamgir joined Meesha Shafi, Strings, Ali Azmat and Shahzad Hasan as a judge on the immensely popular singing talent show \"Music Icons\" which aired on ARY Digital TV channel.\n\n[Mor Mahal]\nThe serial stars Umair Jaswal, Meesha Shafi Hina Khawaja Bayat, Sania Saeed and Fiza Ali in the lead roles.\n\n[Aaina (album)]\nAaina is a musical album produced by Pakistani musician and singer, Alamgir from the soundtrack of the first ground-breaking and the longest running Urdu-language Pakistani movie of the same name in 1976.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q71a71e0593",
  "kind": "yes/no",
  "text": "Claim: Kitchen Stories is a 2003 Norwegian film by this director. This director has more creative titles than the director of Sword of Penitence.\n\nPassages:\n\n[Bent Hamer]\nBent Hamer (born 18 December 1956) is a film director, writer and producer, born in Sandefjord, Norway in 1956.\n\n[Sword of Penitence]\nSword of Penitence (Zange no yaiba: 懺悔の刃 ) is a 1927 Japanese silent film written and directed by Yasujirō Ozu.\n\n[Yasujirō Ozu]\nYasujirō Ozu (小津 安二郎 , Ozu Yasujirō , 12 December 1903 – 12 December 1963) was a Japanese film director and screenwriter.\n\n[Kitchen Stories]\nKitchen Stories (Norwegian: Salmer fra Kjøkkenet ) is a 2003 Norwegian film by Bent Hamer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qf814fc52d6",
  "kind": "yes/no",
  "text": "Claim: The team in the 2013 Alamo Bowl was not led by former American football coach Mark August Helfrich who is currently a college football analyst for Fox Sports.\n\nPassages:\n\n[2013 Alamo Bowl]\nThe 21st edition of the Alamo Bowl, it featured the Texas Longhorns from the Big 12 Conference and the Oregon Ducks from the Pac-12 Conference.\n\n[2013 Oregon Ducks football team]\nThe team was led by first year head coach Mark Helfrich and played their home games at Autzen Stadium for the 47th consecutive year.\n\n[Mark Helfrich (American football)]\nMark August Helfrich (born October 28, 1973) is a former American football coach and is currently a college football analyst for Fox Sports.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qf6daecb7a1",
  "kind": "yes/no",
  "text": "Claim: 8½ is the semi-autobiographical film on which is based the 2009 romantic musical drama, which features an ensemble cast including the English actress Vivian Smith who made her debut with the Old Vic Company.\n\nPassages:\n\n[Nine (2009 live-action film)]\nNine is a 2009 romantic musical drama film directed and produced by Rob Marshall and written by Michael Tolkin and Anthony Minghella. The film is an adaptation of the 1982 musical of the same name, which in turn is based on Federico Fellini's semi-autobiographical 1963 film \"8½\".\n\n[Judi Dench]\nDame Judith Olivia \"Judi\" Dench, {'1': \", '2': \", '3': \", '4': \"} (born 9 December 1934) is an English actress and author. Dench made her professional debut in 1957 with the Old Vic Company.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qae67606711",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "i’m going to cut off contact with every single person i know and emerge in a few months o a year from now having lost the ability to physically speak but be able to play the meanest fucking accordion you’ve ever heard in your pathetic little life",
   "I wish I could take time for myself to heal in the ways that I need to and emerge from it being able to play the accordion."
  ]
 },
 {
  "qid": "q65405c99f9",
  "kind": "yes/no",
  "text": "Claim: The American art critic that met Joseph Drapell died after the death of Agatha Christie.\n\nPassages:\n\n[Joseph Drapell]\nAt the Cranbrook Academy he met visiting Canadian artist Jack Bush and the American art critic Clement Greenberg, who influenced his work.\n\n[Agatha Christie]\nDame Agatha Mary Clarissa Christie, Lady Mallowan, DBE (\"née\" Miller; 15 September 1890 – 12 January 1976) was an English crime novelist, short story writer and playwright.\n\n[Clement Greenberg]\nClement Greenberg ( ), occasionally writing under the pseudonym K. Hardesh (January 16, 1909 – May 7, 1994), was an American essayist known mainly as an influential visual art critic closely associated with American Modern art of the mid-20th century.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q20c2295d74",
  "kind": "yes/no",
  "text": "Claim: The middle name of the actor who hosted the24th People's Choice Awards with Reba McEntire is Albert.\n\nPassages:\n\n[Ray Romano]\nRaymond Albert Romano (born December 21, 1957) is an American stand-up comedian, actor and screenwriter.\n\n[24th People's Choice Awards]\nThey were hosted by Reba McEntire and Ray Romano, and broadcast on CBS.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q1c079dae2d",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "“If I could have changed anything about my childhood I would have never watched spongebob” -no one",
   "\"I don't think anyone regrets watching Spongebob as a child\""
  ]
 },
 {
  "qid": "q89c3e83c55",
  "kind": "yes/no",
  "text": "Claim: R.D. Reid acted in the original version of a movie by director Zack Snyder and featured actor Kevin Zegers, and not the remake by George A. Romero.\n\nPassages:\n\n[Kevin Zegers]\nHe also starred in the films \"Dawn of the Dead\" (2004), \"Transamerica\" (2005), \"It's a Boy Girl Thing\" (2006), \"The Jane Austen Book Club\" (2007), \"Fifty Dead Men Walking\" (2008), and \"Frozen\" (2010).\n\n[R. D. Reid]\nHe appeared in Zack Snyder's \"Dawn of the Dead\", and George A. Romero's \"Diary of the Dead\".\n\n[Dawn of the Dead (2004 film)]\nA remake of George A. Romero's 1978 film of the same name, it was written by James Gunn and stars Sarah Polley, Ving Rhames, Jake Weber, and Mekhi Phifer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q21dcdfffb3",
  "kind": "yes/no",
  "text": "Claim: James Matheson received an award in 2011 which was named after someone who died in October 1954.\n\nPassages:\n\n[Charles Ives]\nCharles Edward Ives ( ; October 20, 1874May 19, 1954) was an American modernist composer.\n\n[James Matheson (composer)]\nJames Matheson (born 1970 in Des Moines, Iowa) is an American composer. In December 2011, he received the Charles Ives Living from the American Academy of Arts and Letters, an award providing him with $100,000 for two years (2012-2014).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qcb71f8a5e9",
  "kind": "yes/no",
  "text": "Claim: The actor who played captain hook in the live production with Taylor Louderman won the academy award for his role in The Deer Hunter.\n\nPassages:\n\n[Christopher Walken]\nWalken has received a number of awards and nominations during his career, including winning the Academy Award for Best Supporting Actor for his portrayal of Nikanor \"Nick\" Chebotarevich in \"The Deer Hunter.\"\n\n[Peter Pan Live!]\nThe special featured a live production of the 1954 musical adaptation of \"Peter Pan\", televised from Grumman Studios in Bethpage, New York, starring Allison Williams in the title role and Christopher Walken as Captain Hook.\n\n[Taylor Louderman]\nIn 2013, she appeared as Wendy in NBC's live production of the musical \"Peter Pan\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q790bacbffb",
  "kind": "yes/no",
  "text": "Claim: Thanjavur is an important religious, art, and architecture city in India and had Pacchimiriam Adiyappa as a court musician in the 18th century.\n\nPassages:\n\n[Pacchimiriam Adiyappa]\nPacchimiriam Adiyappa was a famous court musician at the Maratha kingdom of Thanjavur in the 18th century.\n\n[Thanjavur]\nThanjavur, formerly Tanjore, is a city in the south Indian state of Tamil Nadu. Thanjavur is an important center of South Indian religion, art, and architecture.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qd74d11204b",
  "kind": "yes/no",
  "text": "Claim: The town that was the amusement park that is operated by Britannia Jinky Jersey Ltd located where the first Tomorrow's Parties Festival was held is Camber Sands.\n\nPassages:\n\n[All Tomorrow's Parties (festival)]\nIt was founded by Barry Hogan, in 2001 in preparation for the first All Tomorrow's Parties Festival, the line-up of which was curated by Mogwai and took place at Pontins, Camber Sands, England.\n\n[Pontins]\nPontins is the trading name of Britannia Jinky Jersey Ltd, a company operating holiday parks in the UK.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2140319906",
  "kind": "yes/no",
  "text": "Claim: Don Johnson, born in 1943, was an actor in Miami Vice. He also starred in a movie with Peter Maloney in 1980.\n\nPassages:\n\n[Don Johnson]\nHe played the role of James \"Sonny\" Crockett in the 1980s television series \"Miami Vice\" and had the eponymous lead role in the 1990s cop series \"Nash Bridges\".\n\n[Revenge of the Stepford Wives]\nIt was directed by Robert Fuest with a screenplay by David Wiltse and starring Sharon Gless, Julie Kavner, Don Johnson, Arthur Hill, and Audra Lindley.\n\n[Peter Maloney (actor)]\nHis credits include television series such as \"The Knick\", \"Remember WENN\", and \"Gotham\", and films such as \"Greetings\" (1968), \"Capone\" (1975), \"A Little Romance\" (1979), \"Hide in Plain Sight\" (1980), \"The Children\" (1980), \"Revenge of the Stepford Wives\" (1980), \"The Thing\" (1982), \"Desperately Seeking Susan\" (1985), \"Manhunter\" (1986), \"Tune in Tomorrow\" (1990), \"JFK\" (1991), \"Private Parts\" (1997), \"Boiler Room\" (2000), \"Requiem for a Dream\" (2000), and \"K-PAX\" (2001).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qeb1873c27c",
  "kind": "yes/no",
  "text": "Claim: In the film, The Aristocats, Roddy Maude-Roxby played a character based on a story by a team including Robert Armstrong as a writer.\n\nPassages:\n\n[The Aristocats]\nThe 20th Disney animated feature film, the film is based on a story by Tom McGowan and Tom Rowe, and revolves around a family of aristocratic cats, and how an alley cat acquaintance helps them after a butler has kidnapped them to gain his mistress's fortune which was intended to go to them.\n\n[Roddy Maude-Roxby]\nRoderick A. \"Roddy\" Maude-Roxby (born 2 April 1930 in London) is an English actor who has appeared in numerous films, such as Walt Disney's \"The Aristocats\", where he appeared as Edgar Balthazar; \"Unconditional Love\"; and Clint Eastwood's \"White Hunter Black Heart\", playing Thompson.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa037159df9",
  "kind": "yes/no",
  "text": "Post: I never thought I'd say this, but I have become one of those people who like bounty bars.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qeaa343837c",
  "kind": "yes/no",
  "text": "Claim: Istanbul, Turkey features Endem TV Tower, a 257 m tall tower which once included a revolving restaurant 154 m above ground as well as Cagaloglu Hamam, the last of its kind public hamam built in 1741 to raise revenue by a library.\n\nPassages:\n\n[Cağaloğlu Hamam]\nThe Cağaloğlu Hamam, finished in 1741, is the last hamam to be built in the Ottoman Empire. It was constructed in Istanbul Eminönü, in Alemdar, on Hilal-i Ahmer street as a public hamam to raise revenue for the library of Sultan Mahmud I, previously situated inside the mosque of Ayasofya. It is the last example of its kind to be built in Istanbul and is still operational today.\n\n[Endem TV Tower]\nEndem TV Tower is a TV tower in Beylikdüzü, Istanbul, Turkey. It was built between 1998 and 2002, and has a now closed revolving restaurant 154 m above ground, as well as an observation deck at 160 m . The total height of the tower si 257 m including the antenna.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q273d6dd52b",
  "kind": "yes/no",
  "text": "Claim: Nonso Anozie played a character in the 2016 film A Midsummer Night's Dream. That character was also the name of Silvana opera.\n\nPassages:\n\n[A Midsummer Night's Dream (2016 film)]\nIt stars Maxine Peake as Titania, Matt Lucas as Bottom, John Hannah as Theseus and Nonso Anozie as Oberon.\n\n[Christoph Martin Wieland]\nHe is best-remembered for having written the first Bildungsroman (\"Geschichte des Agathon\"), as well as the epic \"Oberon\", which formed the basis for Carl Maria von Weber's opera of the same name.\n\n[Oberon]\nOberon is a king of the fairies in medieval and Renaissance literature.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q5e9216efbc",
  "kind": "yes/no",
  "text": "Claim: The producer of Back to the World (Street Dogs album), is the Executive Vice President of A&R at this company, while Rod Stewart isn't. The company signed Brian Wilson in 1962.\n\nPassages:\n\n[Nate Albert]\nNate Albert (born 1970) is an American music executive, songwriter, producer and guitar player. He is currently the Executive Vice President of A&R at Capitol Records a division of Universal Music Group.\n\n[Back to the World (Street Dogs album)]\nThe album was produced by Nate Albert, formerly of The Mighty Mighty Bosstones.\n\n[Brian Wilson]\nAfter signing with Capitol Records in 1962, Wilson wrote or co-wrote more than two dozen Top 40 hits for the group.\n\n[Rod Stewart]\nSir Roderick David \"Rod\" Stewart, {'1': \", '2': \", '3': \", '4': \"} (born 10 January 1945) is a British rock singer and songwriter.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q44d9eb1a8e",
  "kind": "yes/no",
  "text": "Claim: Eminem worked with a star of the film 8 Mile and also worked with the artist who played keyboards and wrote songs for Anita Baker.\n\nPassages:\n\n[8 Mile (film)]\n8 Mile is a 2002 American drama film written by Scott Silver, directed by Curtis Hanson, and starring Eminem, Mekhi Phifer, Brittany Murphy, Michael Shannon, and Kim Basinger.\n\n[Luis Resto (musician)]\nLuis Edgardo Resto (born July 22, 1961) is an American musician, producer and keyboardist who has worked closely with rapper Eminem since his third major-label album \"The Eminem Show\". He continued playing keyboards and co-writing songs for a wide variety of artists (including many produced by Don Was), ranging from Anita Baker to Patti Smith to The Highwaymen to Vertical Horizon to Fuel, before beginning a prolific and lengthy collaboration with Eminem in 2001.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qe6522be0e1",
  "kind": "yes/no",
  "text": "Claim: Bassist Chino Moreno has played in more bands than the producer of My Kind Of Evil.\n\nPassages:\n\n[My Kind Of Evil]\nIt was produced by multi-Grammy nominee Kim Wilson (singer for The Fabulous Thunderbirds) and features fellow Canadian Colin James on two tracks.\n\n[Chino Moreno]\nChino Moreno (born Camillo Wong Moreno; June 20, 1973) is an American musician. He is best known as the lead vocalist and contributing guitarist of Deftones. He is also a member of the side-project groups Team Sleep, Crosses, Saudade, and Palms.\n\n[Kim Wilson]\nHe is best known as the lead vocalist and frontman for the Fabulous Thunderbirds on two hit songs of the 1980s, \"Tuff Enuff\" and \"Wrap It Up.\"",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q6670770840",
  "kind": "yes/no",
  "text": "Claim: The star of Australian-Canadian-American satirical comedy, co starting with Ricky Gervais, began his career in sketch comedy series\"Full Frontal\" and also for narrating Stop Laughing...This is Serious.\n\nPassages:\n\n[Eric Bana]\nEric Banadinović (born 9 August 1968), known professionally as Eric Bana, is an Australian actor and comedian.\n\n[Stop Laughing...This Is Serious]\nThe first season of three episodes is narrated by Eric Bana and features a number of well-known comedians and actors who analyse the history of comedy in Australia and relive their own experiences.\n\n[Special Correspondents]\nSpecial Correspondents is a 2016 British-Canadian-American satirical comedy film written, directed by and starring Ricky Gervais.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q3996a1a210",
  "kind": "yes/no",
  "text": "Claim: An assistant coach for the team that Rudy D'Amico scouts for, Under doc rivers and head coach Chuck Daly, led United States men's Olympic basketball team to the gold medal at the 1992 Summer Olympics. Yanni Hufnagel served under this coach.\n\nPassages:\n\n[Rudy D'Amico]\nHe scouts for the Orlando Magic.\n\n[Chuck Daly]\nCharles Jerome Daly (July 20, 1930 – May 9, 2009) was an American basketball head coach. He led the Detroit Pistons to consecutive National Basketball Association (NBA) Championships in 1989 and 1990, and the 1992 United States men's Olympic basketball team (\"The Dream Team\") to the gold medal at the 1992 Summer Olympics.\n\n[Yanni Hufnagel]\nHe last served as an assistant coach of the Nevada Wolf Pack men's basketball team under Eric Musselman.\n\n[Eric Musselman]\nThe son of former NBA head coach Bill Musselman, Eric Musselman was a head coach in the Continental Basketball Association (CBA) before becoming an assistant coach with the Minnesota Timberwolves, Orlando Magic (under Chuck Daly and Doc Rivers), and Atlanta Hawks (under Lon Kruger).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q01a6d173fb",
  "kind": "yes/no",
  "text": "Claim: Hampton's hump and Hampton's line is the name of the conditions that the radiologist who served as chief of radiology at the U.S. Army's flagship medical center from 1909 to 2011.\n\nPassages:\n\n[Aubrey Otis Hampton]\nAubrey Otis Hampton (1900, Copeville, Texas – 1955) was an American radiologist remembered for describing Hampton's hump and Hampton's line. He became chief of radiology at Massachusetts General in 1941, serving as chief of radiology at the Walter Reed Army Hospital in Washington, D.C. from 1942 to 1945.\n\n[Walter Reed Army Medical Center]\nThe Walter Reed Army Medical Center (WRAMC) — known as Walter Reed General Hospital (WRGH) until 1951 — was the U.S. Army's flagship medical center from 1909 to 2011.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q86e9b61d05",
  "kind": "yes/no",
  "text": "Claim: David Michael Bautista Jr the semi-retired professional wrestler appeared in \"Final Score\" .\n\nPassages:\n\n[Final Score (2017 film)]\nFinal Score is an upcoming action film directed by Scott Mann and written by David T. Lynch and Keith Lynch, starring Dave Bautista, who previously worked with Mann in \"Heist\", Ray Stevenson and Pierce Brosnan.\n\n[Dave Bautista]\nDavid Michael Bautista Jr. (born January 18, 1969) is an American actor, semi-retired professional wrestler, former mixed martial artist, and bodybuilder.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q06b0ae9215",
  "kind": "yes/no",
  "text": "Post: Well, my vaccinated therapist tested positive for Covid.  Hope she’s okay and hope my mental health hangs on for 10 extra days.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qbafb736426",
  "kind": "yes/no",
  "text": "Claim: The trainer, who named Eddie Mahan \"the greatest football player of all time\", coached the Indians and was the first Oorang Indians to win a gold metal in his home country.\n\nPassages:\n\n[Eddie Mahan]\nHe was widely regarded as one of the greatest football players in the first 50 years of the sport and was named by Jim Thorpe as the greatest football player of all time.\n\n[Jim Thorpe]\nA member of the Sac and Fox Nation, Thorpe became the first Native American to win a gold medal for his home country.\n\n[Eagle Feather]\nThe Indians were a team based in LaRue, Ohio, composed only of Native Americans, and coached by Jim Thorpe.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 }
]
