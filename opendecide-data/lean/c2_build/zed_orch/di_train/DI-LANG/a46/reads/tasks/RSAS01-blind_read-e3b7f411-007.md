# A46 replay label-noise blind read RSAS01-blind_read-e3b7f411-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS01-blind_read-e3b7f411-007.json

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
  "qid": "q6345e0bd88",
  "kind": "yes/no",
  "text": "Claim: The author of \"We Were Soldiers Once… And Young\" received the Distinguished Coast Guard military decoration for valor.\n\nPassages:\n\n[We Were Soldiers]\nIt is based on the book \"We Were Soldiers Once… And Young\" (1992) by Lieutenant General (Ret.)\n\n[Hal Moore]\nHe was a recipient of the Distinguished Service Cross, which is the U.S. military's second highest decoration for valor, and was the first of his West Point class (1945) to be promoted to brigadier general, major general, and lieutenant general.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q796f85a9c7",
  "kind": "yes/no",
  "text": "Claim: The city in which Benton County State Bank Building is situated had a total population of 54,462 as of the 2010 United States Census.\n\nPassages:\n\n[Benton County State Bank Building]\nThe Benton County State Bank Building, also known as The Madison Building, located in Corvallis, Oregon, is listed on the National Register of Historic Places.\n\n[Corvallis, Oregon]\nAs of the 2010 United States Census, the population was 54,462.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe4ecd9e1a5",
  "kind": "yes/no",
  "text": "Claim: The university Richard J. Wood is a professor of mathematics at has more campuses than California State Polytechnic University, Pomona.\n\nPassages:\n\n[California State Polytechnic University, Pomona]\nCalifornia State Polytechnic University, Pomona (CPP, Cal Poly Pomona, or Cal Poly) is a public polytechnic university located in Pomona, California, United States.\n\n[Dalhousie University]\nDalhousie University (commonly known as Dal) is a public research university in Nova Scotia, Canada, with three campuses in Halifax, a fourth in Bible Hill, and medical teaching facilities in Saint John, New Brunswick.\n\n[Richard J. Wood]\nRichard J. Wood is a mathematics professor at Dalhousie University in Halifax, Nova Scotia, Canada.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe9c6d5f5a7",
  "kind": "yes/no",
  "text": "Claim: The actress known for her role as Dr. Scott Peters in Rogues' Gallery (Gotham) also starred in the remake of the 1983 scifi miniseries created by Kenneth Johnson. Her nationality is Brazilian American.\n\nPassages:\n\n[V (2009 TV series)]\nA remake of the 1983 miniseries created by Kenneth Johnson, the new series chronicles the arrival on Earth of a technologically-advanced alien species which ostensibly comes in peace, but actually has sinister motives. \"V\" stars Elizabeth Mitchell and Morena Baccarin, and is executive produced by Scott Rosenbaum, Yves Simoneau, Scott Peters, Steve Pearlman, and Jace Hall.\n\n[Rogues' Gallery (Gotham)]\nIn this episode, Gordon (Ben McKenzie) is transferred to Arkham Asylum and tries to avoid a conflict when inmates riot with the help of Dr. Leslie Thompkins (Morena Baccarin).\n\n[Morena Baccarin]\nMorena Silva de Vaz Setta Baccarin (] ; born June 2, 1979) is a Brazilian American actress.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qdc524a6dca",
  "kind": "yes/no",
  "text": "Claim: The Shins are an American indie rock group that first had Jesse Sandoval as the drummer and now has Jon Sortland on drums.\n\nPassages:\n\n[The Shins]\nThe band's current lineup consists of James Mercer (vocals, guitar, songwriter), Jon Sortland (drums), Mark Watrous (guitar), Casey Foubert (guitar), Yuuki Matthews (bass), and Patti King (keyboards).\n\n[Jesse Sandoval]\nJesse Sandoval is the former drummer of American indie rock group The Shins.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q168ca218f3",
  "kind": "yes/no",
  "text": "Claim: Rudolf Khametovich Nureyev directed the Paris Opera Ballet from 1983 to 1989 was its chief choreographer until October 1992, and he gave the tittle of étoile to an active member of the Paris Opera Ballet in 1978.\n\nPassages:\n\n[Isabelle Guérin]\nShe was a member of the Paris Opera Ballet from 1978.\n\n[Rudolf Nureyev]\nRudolf Khametovich Nureyev (Bashkir: Рудольф Хәмит улы Нуриев , Tatar: Рудольф Хәмит улы Нуриев , Russian: Рудо́льф Хаме́тович Нуре́ев ; 17 March 1938 – 6 January 1993) was a Soviet ballet dancer and choreographer. He was director of the Paris Opera Ballet from 1983 to 1989 and its chief choreographer until October 1992.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q4335d313b6",
  "kind": "yes/no",
  "text": "Claim: The Waputik Mountains are a mountain range of the Canadian Rockies, named in 1884 by George M. Dawson \"waputik\" is the Bow Indian word for the white goat, which is a white large hoofed mammal endemic to North America.\n\nPassages:\n\n[Mountain goat]\nThe mountain goat (\"Oreamnos americanus\"), also known as the Rocky Mountain goat, is a large hoofed mammal endemic to North America.\n\n[Waputik Mountains]\nNamed in 1884 by George M. Dawson, \"waputik\" is the Stoney Indian word for white goat.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qd4971a65ba",
  "kind": "yes/no",
  "text": "Claim: Polypodium has more species than Cyananthus.\n\nPassages:\n\n[Polypodium]\nPolypodium is a genus of 75–100 species of true ferns, widely distributed throughout the world, with the highest species diversity in the tropics.\n\n[Cyananthus]\nCyananthus is a genus that consists of about 30 species of annual or mostly perennial herbs from high mountains of Central and East Asia.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qb66f66c9e2",
  "kind": "yes/no",
  "text": "Claim: The 247 Cherry building is adjacent to the building that is higher than this building, Stephen M. Ross lives and works there.\n\nPassages:\n\n[Stephen M. Ross]\nRelated is best known for developing the Time Warner Center, where Ross lives and works, as well as the Hudson Yards Redevelopment Project.\n\n[One Manhattan Square]\nOne Manhattan Square (also known as 227 Cherry Street or 250 South Street) is a residential skyscraper project being developed by Extell Development Company in Two Bridges, Manhattan, New York City. The building will stand 80 stories or 850 feet (259 m) above the street, and will possibly have a new supermarket in the tower's base.\n\n[247 Cherry]\nThe building will be adjacent One Manhattan Square.\n\n[Time Warner Center]\nDeveloped by The Related Companies and AREA Property Partners (formerly known as Apollo Real Estate Advisors), its design by David Childs and Mustafa Kemal Abadan of Skidmore, Owings & Merrill, consists of two 750 ft twin towers bridged by a multi-story atrium containing upscale retail shops.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qe8d3523aa7",
  "kind": "yes/no",
  "text": "Claim: This species and the relative of the Fir are classified as genus in the naming system. Parnassius nordmanni is a high altitude butterfly which is found the Caucasus. The larva feeds on this species including \"C. alpestris\", \"C. conorhiza\" and \"C. emanueli\".\n\nPassages:\n\n[Parnassius nordmanni]\nThe larva feeds on \"Corydalis\" species including \"C. alpestris\", \"C. conorhiza\" and \"C. emanueli\".\n\n[Corydalis]\nCorydalis (Greek \"korydalís\" \"crested lark\") is a genus of about 470 species of annual and perennial herbaceous plants in the Papaveraceae family, native to the temperate Northern Hemisphere and the high mountains of tropical eastern Africa.\n\n[Cedrus]\nCedrus (common English name cedar) is a genus of coniferous trees in the plant family Pinaceae.\n\n[Fir]\nFirs are most closely related to the genus \"Cedrus\" (cedar).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qba9ac03bd9",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "we used to make fun of rich men for using 3in1 turns out they were never using anything at all 🤮",
   "it's really funny how rich people think that they aren't held to the same personal hygeine standards as normal people"
  ]
 },
 {
  "qid": "q5402afe351",
  "kind": "yes/no",
  "text": "Claim: Actress and athlete Rosario Dawson, of the movie that starred Rachael Leigh Cook, made her film debut in the 1995 teen drama \"Kids\".\n\nPassages:\n\n[Rachael Leigh Cook]\nRachael Leigh Cook (born October 4, 1979) is an American actress, model, voice artist, and producer, who is best known for her starring role in films \"She's All That\" (1999), \"Josie and the Pussycats\" (2001), and the television series \"Into the West\" and \"Perception\", as well as being the voice behind various characters in \"Robot Chicken\" and Tifa Lockhart in the English version of \"\".\n\n[Rosario Dawson]\nShe made her film debut in the 1995 teen drama \"Kids\".\n\n[Josie and the Pussycats (film)]\nThe film is about a young all-female band which signs a record contract with a New York City record label, only to discover that the company does not have the musicians' best interests at heart.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7054a032ac",
  "kind": "yes/no",
  "text": "Claim: The song, Suga Suga, is sampled in \"Sugar\", the 2015 pop rock album of the same name by Robin Schulz.\n\nPassages:\n\n[Sugar (Robin Schulz song)]\n\"Sugar\" is a song by German DJ and record producer Robin Schulz. The song was released in Germany on 17 July 2015, and samples Baby Bash's 2003 single \"Suga Suga\".\n\n[Sugar (Robin Schulz album)]\nSugar is the second studio album by German DJ and record producer Robin Schulz, it was released on 25 September 2015. The album includes the singles \"Headlights\", \"Sugar\", \"Show Me Love\", and \"Heatwave\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qfa76b3cf62",
  "kind": "yes/no",
  "text": "Claim: Sir John Wedderburn and the brother of Henry Benedict Stuart fought in the unsuccessful Jacobite uprising of 1745. This ended with defeat at the conflict in which Simon Fraser, 11th Lord Lovat fought.\n\nPassages:\n\n[Henry Benedict Stuart]\nUnlike his father, James Francis Edward Stuart, and brother, Charles Edward Stuart, Henry made no effort to seize the throne.\n\n[Sir John Wedderburn, 5th Baronet of Blackness]\nSir John Wedderburn, 5th Baronet of Blackness was a Perthshire gentleman who joined the 1745 rebellion of Charles Edward Stuart and, captured at the Battle of Culloden, was afterwards convicted of treason.\n\n[Simon Fraser, 11th Lord Lovat]\nLovat was among the Highlanders defeated at the Battle of Culloden and convicted of treason against the Crown, following which he was sentenced to death and subsequently beheaded.\n\n[Charles Edward Stuart]\nCharles is perhaps best known as the instigator of the unsuccessful Jacobite uprising of 1745, in which he led an insurrection to restore his family to the throne of Great Britain.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q46ce5bd21d",
  "kind": "yes/no",
  "text": "Text: Day 3. Luggage arrived, thanks @AirFranceFR. Non random Hungarian underwear. Talk delivered. Science sated. #metaxa http://t.co/6KPjLezQOF",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q0f4caa0460",
  "kind": "yes/no",
  "text": "Claim: The town of Tepelenë in Badilonjë is located on the banks of the Vjosa River in Gjirokastër County. After a 2015 local government reform a village became part of its municipality. Ismet Toto was originally from this village.\n\nPassages:\n\n[Tepelenë]\nTepelenë (definite Albanian form: \"Tepelena\" ) is a town and a municipality in Gjirokastër County, in the south of Albania. The town is located on the left bank of the Vjosa River, about three kilometres downstream from its union with the Drino.\n\n[Ismet Toto]\nIsmet Toto (Progonat, 1908 - Gjirokastër, 1937) was an Albanian bureaucrat, publicist, writer and revolutionary.\n\n[Progonat]\nProgonat is a village in the former Kurvelesh municipality, Gjirokastër County. At the 2015 local government reform it became part of the municipality Tepelenë.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q19d255ec0d",
  "kind": "yes/no",
  "text": "Claim: Sunrise Avenue and the band, who released the album \"You Could Have It So Much Better \", were neither formed in 2002.\n\nPassages:\n\n[Franz Ferdinand (band)]\nFranz Ferdinand are a Scottish rock band, formed in 2002 and based in Glasgow.\n\n[You Could Have It So Much Better]\nYou Could Have It So Much Better is the second studio album by Scottish indie rock band Franz Ferdinand.\n\n[Sunrise Avenue]\nSunrise Avenue is a Finnish rock band originally formed in 2002 in Helsinki, Finland.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q720366d102",
  "kind": "yes/no",
  "text": "Claim: The public high school at which Freddie James became the head coach was located in the Oak Cliff area of La Grange.\n\nPassages:\n\n[David W. Carter High School]\nDavid Wendel Carter High School (commonly referred to as Dallas Carter) is a public high school located in the Oak Cliff area of Dallas, Texas (USA).\n\n[Freddie James]\nIn 1982 James became head coach at David W. Carter High School in Dallas, Texas.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe74766f347",
  "kind": "yes/no",
  "text": "Text: virgos are leos in a vest",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qab12d8be13",
  "kind": "yes/no",
  "text": "Claim: The drummer belonged to a band called Chiefs of Relief. His band was formed in a English city. Salmon & Gluckstein were founded in this city.\n\nPassages:\n\n[Sex Pistols]\nThe Sex Pistols were an English punk rock band formed in London in 1975.\n\n[Salmon &amp; Gluckstein]\nFounded in London in 1873 by Samuel Gluckstein and Barnett Salmon (1829-1897), they pursued an aggressive expansion to become the largest tobacco sellers in the UK, with over 140 retail outlets.\n\n[Paul Cook]\nPaul Thomas Cook (born 20 July 1956 in Hammersmith, London) is an English drummer and member of the punk rock band the Sex Pistols.\n\n[Chiefs of Relief]\nChiefs of Relief were a British rock group with a unique electro-punk style, punctuated by the guitar work of vocalist Matthew Ashman, and also featuring drummer Paul Cook.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7b0042129c",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "I’m really looking forward to not hugging my friends and family through choice rather than by law.",
   "I would like to continue social distancing and not hugging people ever"
  ]
 },
 {
  "qid": "q7138c424b7",
  "kind": "yes/no",
  "text": "Claim: Sterling Jewelers was bought by another company in 1987. The company also owns Zale Corporation, a Delaware based retailer, along with H. Samuel and Jared.\n\nPassages:\n\n[Signet Jewelers]\nSignet Jewelers owns and operates the companies Zales, Kay Jewelers, and Jared.\n\n[Sterling Jewelers]\nSterling Jewelers is a wholly owned subsidiary of UK-based Signet Jewelers Limited (listed on the New York Stock Exchange under the symbol SIG), having been acquired in 1987.\n\n[Zale Corporation]\nThe Zale Corporation is an American jewelry retailer, incorporated in Delaware in 1993.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q5323638467",
  "kind": "yes/no",
  "text": "Claim: Stolen Harmony is an French film directed by this man. We don't know for a fact that he directed more films than Jon Jost.\n\nPassages:\n\n[Jon Jost]\nJon Jost (born 16 May 1943 in Chicago) is an American independent filmmaker.\n\n[Alfred L. Werker]\nAlfred L. Werker (December 2, 1896 – July 28, 1975) was a film director whose work in movies spanned from 1917 through 1957. After a number of film production jobs and assistant directing, Werker co-directed his first film, \"Ridin' the Wind\" in 1925 alongside director Del Andrews. He was brought in by Fox Film Corporation executives to re-shoot and re-edit Erich von Stroheim's film \"Hello, Sister! \" (1933), co-starring Boots Mallory and ZaSu Pitts.\n\n[Stolen Harmony]\nThe movie climaxes with an exciting car chase and was directed by Alfred L. Werker.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q6fcf1bc1b3",
  "kind": "yes/no",
  "text": "Claim: The university team with the fight song The Minnesota State Rouser has a mascot called Stomper. It began competing in the same conference as the St. Cloud State Huskies in 2008.\n\nPassages:\n\n[Stomper the Maverick]\nStomper the Maverick is the mascot for the Minnesota State Mavericks athletics teams of the Minnesota State University, Mankato and the associated club teams and charities.\n\n[Minnesota State Mavericks]\nMinnesota State began competition in the NSIC in 2008-09, due to the dissolution of the North Central Conference.\n\n[St. Cloud State Huskies]\nThe university is primarily a member of the Northern Sun Intercollegiate Conference (NSIC), and currently sponsors 18 NCAA Division II teams.\n\n[The Minnesota State Rouser]\nIt is played at all Minnesota State Mavericks athletics games, rallies and at many alumni events.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q145e7fa8ef",
  "kind": "yes/no",
  "text": "Claim: The vocalist who released the album Fire on October 16, 2015, and Bobby Fuller both have a career as a songwriter.\n\nPassages:\n\n[Markus Feehily]\nMarkus Michael Patrick Feehily (formerly known as Mark Feehily, born 28 May 1980) is an Irish singer and songwriter.\n\n[Bobby Fuller]\nRobert Gaston Fuller (October 22, 1942 – July 18, 1966) was an American rock singer, songwriter, and guitarist best known for \"Love's Made a Fool of You\" and his cover of \"I Fought the Law\", recorded with his mid-1960s group The Bobby Fuller Four.\n\n[Fire (Markus Feehily album)]\nFire is the debut solo studio album by Irish singer-songwriter and former Westlife vocalist Markus Feehily.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q9ef67cefc4",
  "kind": "yes/no",
  "text": "Claim: The Oppenheimer security hearing explored the associations of the wartime head of New Mexico laboratory.\n\nPassages:\n\n[Oppenheimer security hearing]\nThe Oppenheimer security hearing was a 1954 proceeding by the United States Atomic Energy Commission (AEC) that explored the background, actions, and associations of J. Robert Oppenheimer, the American scientist who had headed the Los Alamos Laboratory during World War II, where he played a key part in the Manhattan Project that developed the atomic bomb.\n\n[J. Robert Oppenheimer]\nOppenheimer was the wartime head of the Los Alamos Laboratory and is among those who are credited with being the \"father of the atomic bomb\" for their role in the Manhattan Project, the World War II undertaking that developed the first nuclear weapons used in the atomic bombings of Hiroshima and Nagasaki.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qdf5c88cfe8",
  "kind": "yes/no",
  "text": "Text: I put on work out clothes then lay on my bed and watch Netflix",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qec2a2569f2",
  "kind": "yes/no",
  "text": "Claim: Bridge of Spies stars a Soviet intelligence agent with the name Rudolf Abel.\n\nPassages:\n\n[Rudolf Abel]\nRudolf Ivanovich Abel (Russian: Рудольф Иванович Абель ), real name Vilyam \"Willie\" Genrikhovich Fisher (Вильям \"Вилли\" Генрихович Фишер), (July 11, 1903 – November 15, 1971) was a Soviet intelligence officer.\n\n[Bridge of Spies (film)]\nSet during the Cold War, the film tells the story of lawyer James B. Donovan, who is entrusted with negotiating the release of Francis Gary Powers—a U.S. Air Force pilot whose U-2 spy plane was shot down over the Soviet Union in 1960—in exchange for Rudolf Abel, a convicted Soviet KGB spy held under the custody of the United States, whom he represented at trial.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q0dfeaaa941",
  "kind": "yes/no",
  "text": "Claim: Light quadricycles (L6e), and electric quadricycles (L7e) are the two categories of the non-electric version of the neighbourhood electric bike.\n\nPassages:\n\n[Motorised quadricycle]\nTwo categories are defined; knowingly light quadricycles (L6e), and heavy quadricycles (L7e).\n\n[Neighborhood Electric Vehicle]\nThe non-electric version of the neighbourhood electric vehicle is the Motorised quadricycle.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q0d98ef6b30",
  "kind": "yes/no",
  "text": "Claim: The man associated with of Day of the Iguana worked as a comedian and not Norman Foster.\n\nPassages:\n\n[Day of the Iguana]\nDay of the Iguana is the third book in the Hank Zipzer series by Henry Winkler and Lin Oliver.\n\n[Henry Winkler]\nHenry Franklin Winkler (born October 30, 1945) is an American actor, director, comedian, producer, and author.\n\n[Norman Foster (director)]\nNorman Foster (born Norman Foster Hoeffer, December 13, 1903 – July 7, 1976) was an American actor, film director and screenwriter.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qbdef83519a",
  "kind": "yes/no",
  "text": "Claim: Maki Nomiya and Conrad Lant are both considered musicians.\n\nPassages:\n\n[Maki Nomiya]\nMaki Nomiya (野宮 真貴 , Nomiya Maki , born March 12, 1960) is a Japanese singer and musician.\n\n[Conrad Lant]\nConrad Thomas Lant (born 15 January 1963), also known by the stage name of Cronos, is an English musician.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qbc87f7b71a",
  "kind": "yes/no",
  "text": "Claim: The 1988 Nirvana album that their cover song Sliver was rereleased on featured many artists. The list of artists includes The Vaselines, Dave Grohl, and Chad Channing.\n\nPassages:\n\n[Sliver (song)]\nDGC re-released the song to radio to support the release of the rarities compilation album \"Incesticide\" in 1992.\n\n[Son of a Gun (EP)]\nSon of A Gun is the debut extended play single by Glasgow alternative rock group The Vaselines. The title-song of this EP came to a wider audience after Nirvana covered it, along with \"Molly's Lips\", on their compilation album \"Incesticide\".\n\n[Incesticide]\nIncesticide is a compilation album by the American grunge band Nirvana. At the time, the majority of the material on \"Incesticide\" was circulating within fan communities (albeit in lower quality). Since the songs were recorded in different sessions and some were recorded when Nirvana did not have a stable formation, the album includes recordings by four different drummers: Chad Channing, Dan Peters, Dale Crover, and Dave Grohl.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q0ca68d3ecf",
  "kind": "yes/no",
  "text": "Claim: Tantrix and Personal Preference are both types of games.\n\nPassages:\n\n[Tantrix]\nTantrix is a hexagonal tile-based abstract game invented by Mike McManaway from New Zealand.\n\n[Personal Preference]\nPersonal Preference is a 1987 board game created by Donal Carlston that involves guessing the order in which a player prefers foods, activities, people, and other items compared to one another.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q30d4f15619",
  "kind": "yes/no",
  "text": "Claim: Defendant (TV Series) is a South Korean television series, who's star was in a film where sports is featured when she made her film debut.\n\nPassages:\n\n[No Breathing]\nNo Breathing () is a 2013 South Korean sports film set in the world of competitive swimming, starring Seo In-guk, Lee Jong-suk and Kwon Yuri.\n\n[Kwon Yu-ri]\nIn 2013, she made her film debut in \"No Breathing\".\n\n[Defendant (TV series)]\nDefendant () is a South Korean television series starring Ji Sung with Um Ki-joon, Kwon Yu-ri, Oh Chang-seok and Uhm Hyun-kyung.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q12dd49c85a",
  "kind": "yes/no",
  "text": "Claim: An actress who played Micki in \"Micki & Maude\" starred in a 1969 Broadway production. The music for this production was by a man born in April 6, 1929.\n\nPassages:\n\n[Micki &amp; Maude]\nIt co-stars Tony Award-winning actress and dancer Ann Reinking as Micki and Amy Irving as Maude.\n\n[Ann Reinking]\nHer extensive work in musical theater includes starring in Broadway productions of \"Coco\" (1969), \"Over Here!\n\n[André Previn]\nAndré George Previn, KBE ( ; born Andreas Ludwig Priwin; April 6, 1929) is a German-American pianist, conductor, and composer.\n\n[Coco (musical)]\nCoco was a 1969 Broadway musical with a book and lyrics by Alan Jay Lerner and music by André Previn, inspired by the life of Coco Chanel.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q35fc612b3c",
  "kind": "yes/no",
  "text": "Claim: Katrina Szish held a position at a fashion magazine. That magazine was founded before Midwest Living.\n\nPassages:\n\n[Katrina Szish]\nSzish has a prestigious background in journalism, which she has held numerous positions at fashion magazines, including YM, VOGUE, and GQ magazine.\n\n[Midwest Living]\nFounded in 1986, the magazine is dedicated to providing its readers a wealth of region-specific information and inspiration, focusing on travel and events, food and dining, and home and garden, as well as other editorial content categories.\n\n[YM (magazine)]\nYM was an American teen magazine that began in 1932.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8c208fb717",
  "kind": "yes/no",
  "text": "Claim: The Nobel laureate who wrote The Captive Mind, and Nathalie Sarraute do not have the same nationality.\n\nPassages:\n\n[The Captive Mind]\nThe Captive Mind (Polish: Zniewolony umysł ) is a 1953 work of nonfiction by Polish writer, academic and Nobel laureate Czesław Miłosz, published in the English translation originally by Secker and Warburg.\n\n[Czesław Miłosz]\nCzesław Miłosz ( ; 30 June 1911 – 14 August 2004) was a Polish poet, prose writer, translator and diplomat.\n\n[Nathalie Sarraute]\nNathalie Sarraute (] ; July 18, 1900 – October 19, 1999) was a French lawyer and writer.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q912d57aae7",
  "kind": "yes/no",
  "text": "Claim: The Republican Chairman born June 1, 1956, was a sponsor of The Keeping All Students Safe Act with Tom Harkin and George Miller.\n\nPassages:\n\n[Keeping All Students Safe Act]\nThe primary sponsors of the two bills are Senator Tom Harkin (D-IA), Chair of the Senate Health, Education, Labor, and Pensions Committee, Congressman George Miller (D-CA), Ranking Member of the House Education and Workforce Committee, and Congressman Gregg Harper (R-MS).\n\n[Gregg Harper]\nGregory Livingston Harper (born June 1, 1956) is the U.S. Representative for Mississippi 's 3 congressional district , serving since 2009.\n\n[Charlie Ross (state senator)]\nIn 2008, Ross ran for Congress in Mississippi's 3rd congressional district, but was defeated in the primary by Rankin County Republican Chairman Gregg Harper.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q960436957f",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Non sarcastically I would say \"I hate it when people try and get in between me and my friends\"",
   "Love it wen people try and stop my friends seeing me! Looooolll."
  ]
 },
 {
  "qid": "q6a2085806d",
  "kind": "yes/no",
  "text": "Post: What kind of sins have y’all been committing for God to punish us with this kinda weather...",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qc3908eb625",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which version is written sarcastically?",
  "options": [
   "you like ketchup but not tomatoes??? grow up",
   "It seems childish to enjoy ketchup but not tomatoes"
  ]
 },
 {
  "qid": "q7607a1bae8",
  "kind": "yes/no",
  "text": "Tweet: 4-0 this morning, 0-1 this afternoon. Luck possibly changing.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qb478055ddf",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "cold ears? take out one AirPod, leave it by the stove, and forget about it for 20 minutes 🤗",
   "I left my Airpods out by the fire and now my ears are warm."
  ]
 },
 {
  "qid": "q84ead7f76f",
  "kind": "yes/no",
  "text": "Claim: Tom Olivadotti was the defensive coordinator for this Florida team during the championship game. The coach of the team was born in 1934.\n\nPassages:\n\n[Tom Olivadotti]\nHe coached in college for the Princeton Tigers, Boston College Eagles and Miami Hurricanes, where he was the defensive coordinator for the 1983 championship team.\n\n[Howard Schnellenberger]\nHoward Leslie Schnellenberger (born March 16, 1934) is a retired American football coach with long service at both the professional and college levels.\n\n[1983 Miami Hurricanes football team]\nLed by fifth-year head coach Howard Schnellenberger, the Hurricanes finished the season with a record of 11–1 after defeating the Nebraska Cornhuskers in the Orange Bowl.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qcf09e7a351",
  "kind": "yes/no",
  "text": "Text: . @atptour The wearing and non-wearing of face masks by support team and family of players at ATP events is shockingly bad and setting a really poor example to anyone watching. Is it within your remit to encourage or enforce better adherence to effective face mask wearing?",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q92fb7b276c",
  "kind": "yes/no",
  "text": "Claim: The award winning game Doom is a reboot of the franchise developed by id Software.\n\nPassages:\n\n[2016 in video gaming]\nMany awards went to games such as \"Overwatch\", \"\", \"Inside\", \"Doom\", \"Dark Souls III\", \"The Last Guardian\", \"Dishonored 2\" and \"Titanfall 2\".\n\n[Doom (2016 video game)]\nA reboot of the \"Doom\" franchise, it is the fourth title in the main series and the first major installment since \"Doom 3\" in 2004.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qccc5e68f52",
  "kind": "yes/no",
  "text": "Claim: Jeff Alexander Leach who starred in HBO Games of Thrones, is an English actor, writer and comedian. He was born 12 February 1984.\n\nPassages:\n\n[Nell Williams]\nIn 2015 she portrayed a younger version of Cersei Lannister (portrayed by Lena Headey as an adult) in flashback sequences of the opening episode of Season 5 of the HBO series \"Game of Thrones\".\n\n[Cersei Lannister]\nCersei Lannister is a fictional character in the \"A Song of Ice and Fire\" series of fantasy novels by American author George R. R. Martin, and its television adaptation \"Game of Thrones\", where she is portrayed by Lena Headey.\n\n[Jeff Leach]\nHe is most well known for appearing in feature films \"The Smoke\" as Dean and \"London Town\" as Ronnie.\n\n[London Town (2016 film)]\nThe film stars Daniel Huttlestone, Dougray Scott, Natascha McElhone, Nell Williams, and Jonathan Rhys Meyers.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qb2d08521ed",
  "kind": "yes/no",
  "text": "Claim: The man Tony Bennet called \"The Father of Rock and Roll\" once toured with Lola Dee who once auditioned for \"Junior Junction\", and landed a recording contract in her teens.\n\nPassages:\n\n[Lola Dee]\nLola Dee is an American singer and recording artist with Mercury Records and Columbia Records labels in the 1950s and 1960s. At the age of 14, she was heard in an amateur contest and asked to audition for a network teen-aged show called \"Junior Junction\". At 16 she was signed to a recording contract. She recorded over 40 sides, including the half million best seller \"Only You\" in 1955. Her popularity as a recording artist gave her the opportunity to tour with such stars as Bob Hope, Johnnie Ray and Jimmy Durante in the late 1950s and 1960s.\n\n[Johnnie Ray]\nJohn Alvin Ray (January 10, 1927 – February 24, 1990) was an American singer, songwriter, and pianist. Extremely popular for most of the 1950s, Ray has been cited by critics as a major precursor to what would become rock and roll, for his jazz and blues-influenced music and his animated stage personality. Tony Bennett called Ray the \"father of rock and roll,\" and historians have noted him as a pioneering figure in the development of the genre.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3356deacf8",
  "kind": "yes/no",
  "text": "Claim: The company that produced rectangular crackers that have 18 holes in a 3x6 pattern was founded in 1853.\n\nPassages:\n\n[Club Crackers]\nClub Crackers are a brand of crackers made by the American Keebler Company. They are somewhat similar in resemblance to saltines, but are rectangular and have 18 holes in a 3x6 pattern instead of the 13 holes in a 3-2-3-2-3 pattern that are on a saltine.\n\n[Keebler Company]\nThe Keebler Company is the largest cookie and cracker manufacturer in the United States. Founded in 1853, it has produced numerous baked snacks. Keebler has marketed its brands such as Cheez-It (which have the Sunshine Biscuits brand), Chips Deluxe, Club Crackers, E.L. Fudge Cookies, Famous Amos, Fudge Shoppe Cookies, Murray cookies, Austin, Plantation, Vienna Fingers, Town House Crackers, Wheatables, Sandie's Shortbread, Chachos and Zesta Crackers, among others.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5f6b1c2b37",
  "kind": "yes/no",
  "text": "Claim: Robert Gibson is the name of the one of the hosts of the Race for the Pennant television show who is a retired american league pitcher.\n\nPassages:\n\n[Bob Gibson]\nRobert Gibson (born November 9, 1935) is a retired American baseball pitcher who played 17 seasons in Major League Baseball (MLB) for the St. Louis Cardinals (1959–75).\n\n[Race for the Pennant]\nRace for the Pennant is a weekly sports show that focused on Major League Baseball and premiered on Home Box Office (HBO) in 1978. It was hosted by Len Berman, Tim McCarver, Barry Tompkins, Bob Gibson, Maury Wills and others.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 }
]
