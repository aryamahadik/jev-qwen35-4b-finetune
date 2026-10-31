# A46 replay label-noise blind read RSBS01-blind_read-9bc18c82-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS01-blind_read-9bc18c82-000.json

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
  "qid": "qb2715a85e3",
  "kind": "yes/no",
  "text": "Claim: One of the founding members of the Breeders was the singer for Throwing Muses. She was born 4 years before Trace Cyrus.\n\nPassages:\n\n[Tanya Donelly]\nTanya Donelly (born July 14, 1966, in Newport, Rhode Island) is an American Grammy Award-nominated singer-songwriter and guitarist based in New England who co-founded Throwing Muses with her stepsister Kristin Hersh.\n\n[The Breeders]\nThe Breeders are an American alternative rock band formed in 1989 by Kim Deal of the Pixies and Tanya Donelly of Throwing Muses.\n\n[Trace Cyrus]\nTrace Dempsey Cyrus (born Neil Timothy Helson; February 24, 1989) is an American musician.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qd968cb1bb9",
  "kind": "yes/no",
  "text": "Claim: Ralf D. Bode is best known for his work on a film starring Sissy Spacek as Loretta.\n\nPassages:\n\n[Coal Miner's Daughter (film)]\nIt stars Sissy Spacek as Loretta, a role that earned her the Academy Award for Best Actress.\n\n[Ralf D. Bode]\nRalf Detlef Bode (March 31, 1941 – February 27, 2001) was a German-born American cinematographer best known for his Academy Award nominated work on \"Coal Miner's Daughter\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q1a46aee68d",
  "kind": "yes/no",
  "text": "Claim: Ahmad Niyaltigin was the treasurer of a sultan who rose to power by seizing the Ghaznavid throne from his younger twin.\n\nPassages:\n\n[Ahmad Niyaltigin]\nAhmad Niyaltigin (Persian: ‎ ‎ ) was a treasurer of Sultan Mahmud Ghaznavi and later of his son Sultan Mas'ud Ghaznavi.\n\n[Mas'ud I of Ghazni]\nMas'ud I of Ghazni (Persian: مسعود غزنوی‎ ‎ ), known as Amīr-i Shahīd (امیر شهید ; \"the martyr king\")(998 – 17 January 1040), was \"sultan\" of the Ghaznavid Empire from 1030 to 1040. He rose to power by seizing the Ghaznavid throne from his younger twin Mohammad, who had been nominated as the heir upon the death of their father Mahmud of Ghazni.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q2b25be845e",
  "kind": "yes/no",
  "text": "Post: My (extended) fam was discussing going on a trip instead of getting presents for Christmas, like okay I’m bout it...\nYeah they were talking about doing to the dells. I’ll take my god damn presents thank you very much",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q1a29eac779",
  "kind": "yes/no",
  "text": "Claim: The 247 Cherry building is adjacent to the building that is higher than this building, Stephen M. Ross lives and works there.\n\nPassages:\n\n[Stephen M. Ross]\nRelated is best known for developing the Time Warner Center, where Ross lives and works, as well as the Hudson Yards Redevelopment Project.\n\n[One Manhattan Square]\nOne Manhattan Square (also known as 227 Cherry Street or 250 South Street) is a residential skyscraper project being developed by Extell Development Company in Two Bridges, Manhattan, New York City. The building will stand 80 stories or 850 feet (259 m) above the street, and will possibly have a new supermarket in the tower's base.\n\n[247 Cherry]\nThe building will be adjacent One Manhattan Square.\n\n[Time Warner Center]\nDeveloped by The Related Companies and AREA Property Partners (formerly known as Apollo Real Estate Advisors), its design by David Childs and Mustafa Kemal Abadan of Skidmore, Owings & Merrill, consists of two 750 ft twin towers bridged by a multi-story atrium containing upscale retail shops.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qd098d0ada0",
  "kind": "yes/no",
  "text": "Text: Vaccinated this morning. Not sure it's worked - still committed to Apple and no extra autism detected. Bloody science.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q82ae0eb533",
  "kind": "yes/no",
  "text": "Claim: Sevilla Atlético football team that was relegated to Tercera División in the 1962–63 Segunda División season was founded in October of 1958.\n\nPassages:\n\n[1962–63 Segunda División]\nBaskonia, Sabadell, Sevilla Atlético, Plus Ultra, Atl. Baleares, Cartagena and Real Jaén were relegated to Tercera División.\n\n[Sevilla Atlético]\nFounded in 1958 it plays in Segunda División and is the reserve team of Sevilla FC, holding home games at \"Viejo Nervión\", with a 7,500-seat capacity.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q935e10834a",
  "kind": "yes/no",
  "text": "Claim: William Davis Ticknor, Sr. served on the board of a chemical and biotechnology company created in 1919.\n\nPassages:\n\n[Commercial Solvents Corporation]\nCommercial Solvents Corporation (CSC) was an American chemical and biotechnology company created in 1919.\n\n[William Davis Ticknor, Sr.]\nWilliam Davis Ticknor, Sr. (January 11, 1881 – March 24, 1938) was president and chairman of the board of Commercial Solvents Corporation.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q935ea340fb",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "No longer a female as I refuse to wear heels ever again",
   "I refuse to wear heels ever again because they hurt too much."
  ]
 },
 {
  "qid": "q86b1a05512",
  "kind": "yes/no",
  "text": "Claim: Chindia is a portmanteau word that refers to China and India together in general, together, they contain over one-third of the total number of humans currently living, and is called world's population.\n\nPassages:\n\n[Chindia]\nTogether, they contain over one-third of the world's population (nearly 2.7 billion).\n\n[World population]\nIn demographics, the world population is the total number of humans currently living.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa391fc500b",
  "kind": "yes/no",
  "text": "Claim: The 2001 standard that defines the list of mammals with 17 mammal species is similar to UN M.49 standard that originated in the United Nations Statistics Division.\n\nPassages:\n\n[Svalbard and Jan Mayen]\nSvalbard and Jan Mayen (Norwegian: \"Svalbard og Jan Mayen\" , ISO 3166-1 alpha-2: SJ, ISO 3166-1 alpha-3: SJM, ISO 3166-1 numeric: 744) is a statistical designation defined by ISO 3166-1 of two parts of Norway under separate jurisdictions—Svalbard and Jan Mayen.\n\n[ISO 3166-1 numeric]\nThey are similar to the three-digit country codes developed and maintained by the United Nations Statistics Division, from which they originate in its UN M.49 standard.\n\n[List of mammals of Svalbard and Jan Mayen]\nThere are 17 mammal species in Svalbard and Jan Mayen, of which 0 are critically endangered, 3 are endangered, 3 are vulnerable, and 0 are near-threatened.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qd71c592640",
  "kind": "yes/no",
  "text": "Claim: Jeremiah Joseph O'Keefe was mayor in Harrison County from 1973 to 1981.\n\nPassages:\n\n[Biloxi, Mississippi]\nBiloxi ( ) is a city in Harrison County, Mississippi, United States.\n\n[Jeremiah Joseph O'Keefe]\nIn addition, he served as a member of the Mississippi House of Representatives and was the mayor of Biloxi, Mississippi from 1973 to 1981.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qcdd6d665ec",
  "kind": "yes/no",
  "text": "Claim: Douglas county in Minnesota holds a 202 lb slab of greywacke covered in runes.\n\nPassages:\n\n[Kensington, Minnesota]\nKensington is a city in Douglas County, Minnesota, United States. The city is notable in Minnesota history for being the place where the famous, if questionable, Kensington Runestone was first displayed.\n\n[Kensington Runestone]\nThe Kensington Runestone is a 202 lb slab of greywacke covered in runes on its face and side.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qdd014b2d94",
  "kind": "yes/no",
  "text": "Claim: Makbule Atadan was the older sister of a Turkish army officer whose policies and theories became known as Kemalism.\n\nPassages:\n\n[Makbule Atadan]\nMakbule Atadan (1885 – January 18, 1956) was the sister of Mustafa Kemal Atatürk, the founder of the Republic of Turkey.\n\n[Mustafa Kemal Atatürk]\nMustafa Kemal Atatürk (] ; 19 May 1881 – 10 November 1938) was a Turkish army officer, revolutionary, and founder of the Republic of Turkey, serving as its first President from 1923 until his death in 1938. Ideologically a secularist and nationalist, his policies and theories became known as Kemalism.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q2bddfb2af2",
  "kind": "yes/no",
  "text": "Claim: A breed the of dog was developed in New London, Wisconsin. That breed was derived before the Estonian Hound.\n\nPassages:\n\n[New London, Wisconsin]\nThe American Water Spaniel was developed as a registered breed by F. J. Pfeifer of New London.\n\n[American Water Spaniel]\nThe breed was saved by Dr. Fred J. Pfeifer, who set up the breed club and standard, and whose work led to recognition for the breed by the United Kennel Club, and later, the American Kennel Club.\n\n[Estonian Hound]\nIt was bred in 1947 when the Soviet Union's national economy ministry decided that every country in the Union must have its own dog breed.\n\n[English Water Spaniel]\nThe English Water Spaniel is a breed of dog that has been extinct since the first part of the 20th century, with the last specimen seen in the 1930s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q66a2e83208",
  "kind": "yes/no",
  "text": "Claim: In 2011 the population of the town where the band with a compilation double album called 24 Carat Purple were formed was about 26,000.\n\nPassages:\n\n[Hertford]\nForming a civil parish, the 2011 census put the population of Hertford at about 26,000.\n\n[24 Carat Purple]\n24 Carat Purple is the first compilation album of the hard rock band Deep Purple released worldwide on their own record company and the third in a long line of compilation albums.\n\n[Deep Purple]\nDeep Purple are an English rock band formed in Hertford in 1968.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q38452a5888",
  "kind": "yes/no",
  "text": "Claim: The film where Razak Khan played Manikchand, is an Indian film that was inspired by Mr. Nice Guy, a Hong Kong action movie starring Jackie Chan and Richard Norton.\n\nPassages:\n\n[Razak Khan]\nHe was known for his comic role of Manikchand in the 1999 Abbas-Mustan directed film \"Baadshah\", as Ninja Chacha in the 1999 film \"Hello Brother\", and as Takkar Pehelwan in \"Akhiyon Se Goli Maare\".\n\n[Mr. Nice Guy (1997 film)]\nMr. Nice Guy (一個好人, LSHK \"Jat1 go3 hou2 jan4\") is a 1997 Hong Kong action film directed by Sammo Hung, who makes a cameo as an unfortunate cyclist. The film stars Jackie Chan and Richard Norton.\n\n[Baadshah (1999 film)]\nBaadshah (translation: \"King\") is a 1999 Indian action comedy film directed by Abbas-Mustan. It is inspired from films such as \"Nick of Time\", \"Rush Hour\", \"If Looks Could Kill\", \"Mr Nice Guy\", \"The Mask\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q665d405093",
  "kind": "yes/no",
  "text": "Claim: The singer in which Jorge Salan played lead guitarist for in an European tour originates in the city of Brooklyn in the confederated state of new York.\n\nPassages:\n\n[Robin Beck]\nRobin Beck (born November 7, 1954 in Brooklyn, New York) is an American singer.\n\n[Jorge Salán]\nHe is most well known for being the lead guitar for the metal rock solo singer Jeff Scott Soto (leading voice of Journey, Yngwie Malmsteen) and the Jeff Scott Soto Band (now SOTO) from 2009 till today, the lead guitar on Robin Beck's European Tour 2013, and for having collaborated with a long list of legendary rock musicians such as Fiona Flanagan or bass guitar player Bob Daisley.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qf1e5766440",
  "kind": "yes/no",
  "text": "Claim: The grandfather of Rainer Hoss conducted the negotiations with the owners and was the longest serving commandant of Lublin concentration and extermination camp.\n\nPassages:\n\n[Rainer Höss]\nRainer Höss, born 25 May 1965 in Stuttgart, is the grandson of Rudolf Höss.\n\n[Rudolf Höss]\nRudolf Höss (also Höß, Hoeß or Hoess; 25 November 1901 – 16 April 1947) was a Nazi German \"SS\"-\"Obersturmbannführer\" (lieutenant colonel) and the longest-serving commandant of Auschwitz concentration and extermination camp in World War II.\n\n[Gerstein Report]\nThe Gerstein Report was written in 1945 by Kurt Gerstein, an Obersturmführer (First Lieutenant) of the Waffen-SS who rose to become the Head of Technical Disinfection Services of the SS, and in that capacity supplied hydrogen cyanide (Zyklon B) from Degesch (\"Deutsche Gesellschaft für Schädlingsbekämpfung\") to Rudolf Höss in Auschwitz and conducted the negotiations with the owners.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q835c380d28",
  "kind": "yes/no",
  "text": "Claim: Wincenty Gostkowski was a lawyer for the watch manufacturer Patek Philippe & Co. in the cityof Geneva in Schaffhausen.\n\nPassages:\n\n[Patek Philippe &amp; Co.]\nPatek Philippe & Co. is a Swiss watch manufacturer founded in 1851, located in Geneva and the Vallée de Joux.\n\n[Wincenty Gostkowski]\nWincenty Gostkowski (March 29, 1807 – August 29, 1884) was a lawyer and associate of Antoni Patek and Adrien Philippe in the watchmaker Patek Philippe & Co. in Geneva, Switzerland.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qd53f7e4955",
  "kind": "yes/no",
  "text": "Claim: Seven years before the construction of the Brewer Fieldhouse in Columbia, Missouri, Chester Brewer worked as head football coach and head basketball coach of University Farm.\n\nPassages:\n\n[Brewer Fieldhouse]\nThe Brewer Fieldhouse was a multi-purpose arena located in Columbia, Missouri, and home to the University of Missouri Tigers basketball team prior to the Hearnes Center opening in 1972. Named after Chester Brewer, the building opened in 1929 to expand on the existing 500 seat Rothwell Gymnasium.\n\n[Chester Brewer]\nHe served as the head football coach at Albion College (1899–1902), Michigan Agricultural College, now Michigan State University, (1903–1910, 1917, 1919), the University of Missouri (1911–1913), and the University Farm, now the University of California, Davis, (1922), compiling a career record of 97–51–4. Brewer was also the head basketball coach at Michigan Agricultural (1903–1910), Missouri (1910–1911) and the University Farm (1922–1923), tallying a mark of 84–36, and the head baseball coach at Michigan Agricultural (1904–1910, 1918–1920) and Missouri (1911, 1914–1917, 1933–1934), amassing a record of 148–93–4.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q119ed20d3e",
  "kind": "yes/no",
  "text": "Claim: Adam Minarovich and Core Harrison own the famous pawn shop d Famous Gold & Silver Pawn Shop.\n\nPassages:\n\n[Corey Harrison]\nRichard Corey \"Big Hoss\" Harrison (born April 27, 1983) is an American businessman and reality television personality, known as a cast member of the History TV series \"Pawn Stars\", which documents his work at the World Famous Gold & Silver Pawn Shop in Las Vegas, which he co-owns with his father, Rick Harrison, and grandfather, Richard Benjamin Harrison.\n\n[Rick Harrison]\nRichard Kevin \"Rick the Spotter\" Harrison (born March 22, 1965) is an American, Las Vegas-based businessman and reality television personality, best known as the co-owner of the World Famous Gold & Silver Pawn Shop, as featured on the History series \"Pawn Stars\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q822f636fd1",
  "kind": "yes/no",
  "text": "Claim: Pocari Sweat and another beverage are both canned drinks. This other beverage was endorsed by a character played by Hugh Manning.\n\nPassages:\n\n[Robinsons (drink)]\nRobinsons is an English fruit drink brand owned by Britvic.\n\n[Hugh Manning]\nHe also starred in the tv series \"Mrs Thursday\", alongside Kathleen Harrison in 1966, playing a suave and imperturbable Butler, which also carried over into popular tv commercials where his character endorsed the qualities of Robinsons barley water.\n\n[Pocari Sweat]\nPocari Sweat (ポカリスエット , Pokari Suetto ) is a Japanese sports drink, manufactured by Otsuka Pharmaceutical It was launched in 1980, and is now also available in East Asia, Southeast Asia, and the Middle East.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q80c4bc3875",
  "kind": "yes/no",
  "text": "Claim: This Hall of Fame point guard was first selected for an Blazers All-Star Game in 1994, alongside Shawn Kemp. He was the Defensive Player of the Year for the Seattle SuperSonics 1995–96 Blazers season.\n\nPassages:\n\n[Gary Payton]\nHe started at the point guard position. He was inducted into the Naismith Basketball Hall of Fame on September 8, 2013.\n\n[1995–96 Seattle SuperSonics season]\nShawn Kemp and Defensive Player of the Year, Gary Payton were both selected for the 1996 NBA All-Star Game.\n\n[1993–94 Seattle SuperSonics season]\nGary Payton made his first All-Star appearance as he was selected for the 1994 NBA All-Star Game along with Shawn Kemp.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qb993b2fac0",
  "kind": "yes/no",
  "text": "Claim: Lookwell was a black & white television pilot written and produced by Conan O'rien and Robert Smigel, and was a personal favorite of Brandon Tartikoff who was president of NBC from 1980-1991.\n\nPassages:\n\n[Lookwell]\nLookwell was a television pilot written and produced by Conan O'Brien and Robert Smigel, the latter of whom would become a primary creative voice for O'Brien's late night show. Despite being a \"personal favorite\" of NBC chairman Brandon Tartikoff, the pilot was not picked up as a series.\n\n[Brandon Tartikoff]\nBrandon Tartikoff (January 13, 1949 – August 27, 1997) was an American television executive who was the president of NBC from 1980 to 1991.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1ac0fbd45b",
  "kind": "yes/no",
  "text": "Tweet: Just made my own pitta chips after whinging at anyone who'd listen that I can't buy them locally. So that's pitta chips and apple crumble in my culinary repertoire. SOMEONE WIFE ME.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q8b0612e14a",
  "kind": "yes/no",
  "text": "Claim: The most important surviving 16th century Byzantine building in Ayakapı and an area in the Faith district are both located in Istanbul, Turkey. This area is also home to the Turkish and Islamic Arts Museum.\n\nPassages:\n\n[Ayakapı]\nIn Ayakapı lies one of the most important surviving Byzantine buildings of the historical peninsula, the Gül Mosque.\n\n[Turkish and Islamic Arts Museum]\nThe Turkish and Islamic Arts Museum (Turkish: \"\" ) is a museum located in Sultanahmet Square in Fatih district of Istanbul, Turkey.\n\n[Gül Mosque]\nGül Mosque (Turkish: \"Gül Camii\" , meaning: \"The Mosque of the Rose\" in English) is a former Eastern Orthodox church in Istanbul, Turkey, converted into a mosque by the Ottomans.\n\n[Hippodrome of Constantinople]\nToday it is a square named \"Sultanahmet Meydanı\" (\"Sultan Ahmet Square\") in the Turkish city of Istanbul, with a few fragments of the original structure surviving.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q1f98142352",
  "kind": "yes/no",
  "text": "Claim: A noteworthy performer produced by All for One Theater was born in Notts County, Montana.\n\nPassages:\n\n[Tom Hewitt (actor)]\nTom Hewitt (born c. 1957) is an American actor and Broadway stage performer, and a native of Victor, Montana.\n\n[All for One Theater]\nNoteworthy performers whom AFO has produced include Tom Hewitt, Deb Margolin, Leslie Jordan, Annabelle Gurwitch, and Bill Bowers.\n\n[Victor, Montana]\nVictor is a census-designated place (CDP) in Ravalli County, Montana, United States.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q03dd97d33b",
  "kind": "yes/no",
  "text": "Claim: The video of the song Die with you is sold only on a streaming platform maintained by the company Aspiro AB.\n\nPassages:\n\n[Die with You]\nThe new video, available only on Tidal, features home footage.\n\n[Tidal (service)]\nThe service is maintained by the Norwegian company Aspiro AB.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8b3775ccbd",
  "kind": "yes/no",
  "text": "Claim: The Birthday of the World: and Other Stories was written by fantasy and sci-fi author Ursula Kroeber Le Guin .\n\nPassages:\n\n[Ursula K. Le Guin]\nUrsula Kroeber Le Guin ( ; born October 21, 1929) is an American author of novels, children's books, and short stories, mainly in the genres of fantasy and science fiction.\n\n[The Birthday of the World: and Other Stories]\nThe Birthday of the World: and Other Stories is a collection of short fiction by American writer Ursula K. Le Guin, first published in March, 2002 by HarperCollins.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q78d348d267",
  "kind": "yes/no",
  "text": "Claim: Lorentz & Sakarias is a hip-hop duo from Stockholm, Sweden, which has collaborated with Swedish actor Gustaf Caspar Orm Skarsgård during the summer of 2009.\n\nPassages:\n\n[Lorentz &amp; Sakarias]\nThey have collaborated with jj, Duvchi, Newkid and Gustaf Skarsgård.\n\n[Gustaf Skarsgård]\nGustaf Caspar Orm Skarsgård (] ; born 12 November 1980) is a Swedish actor.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q8b06ade628",
  "kind": "yes/no",
  "text": "Claim: Marilyn Manson and Joe Lynn Turner are both American singer, songwriters.\n\nPassages:\n\n[Marilyn Manson]\nBrian Hugh Warner (born January 5, 1969), known professionally as Marilyn Manson, is an American singer, songwriter, musician, composer, actor, painter, author and former music journalist.\n\n[Joe Lynn Turner]\nJoe Lynn Turner (born Joseph Arthur Mark Linquito, August 2, 1951) is an American singer, guitarist, songwriter, and producer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q97d77d7bb4",
  "kind": "yes/no",
  "text": "Text: @barcacentre Unemployed and lazy that Messi guy 😂\n\n(I'm being sarcastic guys, I'm warning you lol)",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q291620f072",
  "kind": "yes/no",
  "text": "Post: i’m ALREADY stressed about whose pov to watch for mcc hahah",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qdd2a14f800",
  "kind": "yes/no",
  "text": "Claim: Rex Gene Foods and Foodtown were located in United States.\n\nPassages:\n\n[Foodtown (United States)]\nFoodtown's corporate offices are located in Iselin, New Jersey.\n\n[Rex Gene Foods]\nRex Gene Foods was a United States supermarket chain of stores located in New Jersey from 1957 until the late 1990s.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qeff3a542d0",
  "kind": "yes/no",
  "text": "Claim: An IndyCar race driver drove a Formula 1 car designed by Peter McCool during the 2007 Formula One season.\n\nPassages:\n\n[Super Aguri SA07]\nThe Super Aguri F1 SA07 was Super Aguri F1's Formula One car for the 2007 Formula One season.\n\n[Takuma Sato]\nSato has raced full-time in the IndyCar Series since 2010 for the KV, Rahal, Foyt, and currently Andretti teams.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qfa336fe036",
  "kind": "yes/no",
  "text": "Text: crocheting is hard",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q12f255cdc5",
  "kind": "yes/no",
  "text": "Tweet: Super bummed that one of my best friends from high school is a republican",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q2ecb9d88ea",
  "kind": "yes/no",
  "text": "Claim: The movie that featured the song \"\"Air Buddies\"\" from the album Soul Dancing and Air Bud are American comedy movies.\n\nPassages:\n\n[Air Bud]\nAir Bud is a 1997 American comedy film that sparked the franchise centered on the real-life dog, Buddy, a Golden Retriever.\n\n[Soul Dancing]\nThe song \"I'll Wait\" was featured in the 1994 Disney comedy \"Blank Check\".\n\n[Blank Check (film)]\nBlank Check is a 1994 American comedy film directed by Rupert Wainwright and starring Brian Bonsall, Karen Duffy, Miguel Ferrer, James Rebhorn, Tone Lōc, Jayne Atkinson and Michael Lerner.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q9b5bee1f4e",
  "kind": "yes/no",
  "text": "Claim: The star of Oh, Dear Augustine and Brian Robbins are both actors and film producers.\n\nPassages:\n\n[Oh, Dear Augustine]\nOh, Dear Augustine (German:Oh, du lieber Augustin) is a 1922 Austrian silent film directed by H.K. Breslauer and starring Willi Forst.\n\n[Willi Forst]\nWilli Forst, born Wilhelm Anton Frohs (7 April 1903 – 11 August 1980) was an Austrian actor, screenwriter, film director, film producer and singer.\n\n[Brian Robbins]\nBrian Levine (born November 22, 1963), best known as Brian Robbins, is an American actor, film director, film producer, television director, television producer and occasional screenwriter.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q638dc6f821",
  "kind": "yes/no",
  "text": "Claim: Mark Elliot is a voice-over artist. The central character of a rabbit story he did voice overs for, was later adapted into the 1946 Walt Disney Company motion picture film \"Song of the South\".\n\nPassages:\n\n[The Adventures of Brer Rabbit]\nThe Adventures of Brer Rabbit is a book, a play, and a film inspired by the Uncle Remus stories.\n\n[Mark Elliot (voice-over artist)]\nHe was also the voice of CBS and FOX throughout the 1980s and 1990s, and various theatrical trailers for such non-Disney animated movies as \"All Dogs Go to Heaven\", \"The Seventh Brother\", \"Rover Dangerfield\", \"Rock-A-Doodle\", \"\", \"The Magic Voyage\", \"The Thief and the Cobbler\", \"Once Upon a Forest\", \"The Princess And The Goblin\", \"Andre\", \"Asterix Conquers America\", \"The Swan Princess\", \"The Pagemaster\", \"The Pebble and the Penguin\", \"Balto\", \"All Dogs Go to Heaven 2\", \"Tiny Heroes\" (\"Vacak 2 - az erdő hőse\"), \"Zeus and Roxanne\", \"The Fearless Four\", \"The Prince of Egypt\", \"The Adventures of Brer Rabbit\", \"\", \"House Arrest\", and \"\".\n\n[Br'er Rabbit]\nThe Walt Disney Company later adapted this character for its 1946 animated motion picture \"Song of the South\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qf506967240",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "Life is about happiness and friendship",
   "Life is about eating chicken finger and getting drunk"
  ]
 },
 {
  "qid": "q3f3b496da0",
  "kind": "yes/no",
  "text": "Claim: Peter Staley was the primary figure in the documentary that includes footage of a demonstration at a cathedral. The cathedral was located in New York City.\n\nPassages:\n\n[Peter Staley]\nHe is a primary figure in the Oscar-nominated documentary \"How to Survive a Plague\".\n\n[How to Survive a Plague]\nThe film, which opened in select theatres across the United States on September 21, 2012, also includes footage of a demonstration during mass at St. Patrick's Cathedral in 1989.\n\n[St. Patrick's Cathedral (Manhattan)]\nThe Cathedral of St. Patrick (commonly called St. Patrick's Cathedral) is a decorated Neo-Gothic-style Roman Catholic cathedral church in the United States and a prominent landmark of New York City.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8333efa03e",
  "kind": "yes/no",
  "text": "Claim: The battle in which John W. Minick won the Medal of Honor lasted longer than Battle of Pusan Perimeter.\n\nPassages:\n\n[Battle of Pusan Perimeter]\nThe Battle of Pusan Perimeter was a large-scale battle between United Nations and North Korean forces lasting from August 4 to September 18, 1950.\n\n[Battle of Hürtgen Forest]\nThe Battle of Hürtgen Forest (German: \"Schlacht im Hürtgenwald\" ) was a series of fierce battles fought from 19 September to 16 December 1944 between American and German forces on the Western Front during World War II in the Hürtgen Forest about 50 mi2 east of the Belgian–German border.\n\n[John W. Minick]\nHe was a United States Army soldier and a recipient of the United States military's highest decoration—the Medal of Honor—for his actions during the Battle of Hürtgen Forest in World War II.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc169e1da7b",
  "kind": "yes/no",
  "text": "Claim: Helen Elizabeth Hunt won more awards than Dan Schneider.\n\nPassages:\n\n[Helen Hunt]\nHelen Elizabeth Hunt (born June 15, 1963) is an American actress, director, and screenwriter. She starred in the sitcom \"Mad About You\" for seven years, and played single mother Carol Connelly in the 1997 romantic comedy film \"As Good as It Gets\", for which she won the Academy Award for Best Actress. Hunt has also won four Emmy Awards, four Golden Globe Awards, and two Screen Actors Guild Awards.\n\n[Dan Schneider (TV producer)]\nDan Schneider (born January 14, 1966) is an American actor, television and film writer, and producer. After appearing in mostly supporting roles in a number of 1980s and 1990s films and TV shows, Schneider devoted himself to behind-the-scenes work in production. He is the co-president of television production company Schneider's Bakery. He created/co-created \"All That\", \"The Amanda Show\", \"What I Like About You\", \"Drake & Josh\", \"Zoey 101\", \"iCarly\", \"Victorious\", \"Sam & Cat\", \"Henry Danger\", \"Game Shakers\", and \"The Adventures of Kid Danger and Captain Man\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q1077ce5019",
  "kind": "yes/no",
  "text": "Claim: Snakes on a Plane (Bring It) is the debut dingle for this band. The lead vocalist of this band and Robert Plant are not both English.\n\nPassages:\n\n[Snakes on a Plane (Bring It)]\n\"Snakes on a Plane (Bring It)\", also referred to as \"Bring It (Snakes on a Plane)\", is the debut single by Cobra Starship, released in 2006 from the soundtrack album \"\".\n\n[Gabe Saporta]\nGabriel Eduardo \"Gabe\" Saporta (born October 11, 1979) is an Uruguayan-American musician and entrepreneur.\n\n[Cobra Starship]\nCobra Starship was an American dance-pop band created by former Midtown bassist and lead vocalist Gabe Saporta in 2006 in New York City, New York.\n\n[Robert Plant]\nRobert Anthony Plant, {'1': \", '2': \", '3': \", '4': \"} (born 20 August 1948) is an English singer, songwriter, and musician, best known as the lead singer and lyricist of the rock band Led Zeppelin.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q1d62317bf0",
  "kind": "yes/no",
  "text": "Post: i hope u sleep maybe forever maybe not  lol",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q7c0a8d6b7e",
  "kind": "yes/no",
  "text": "Claim: Now Is Good is a film in which Jeremy Irvine had a role is a 2012 Indian teen drama film directed by Ol Parker.\n\nPassages:\n\n[Now Is Good]\nNow Is Good is a 2012 British teen drama film directed by Ol Parker.\n\n[Jeremy Irvine]\nIn 2012, he portrayed Philip \"Pip\" Pirrip in the film adaptation of \"Great Expectations\", and earned widespread critical acclaim for his role in the independent film \"Now Is Good\" (2012).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q2982830515",
  "kind": "yes/no",
  "text": "Claim: Matt Miller (musician) plays bass in a band. This band and King Charles are not both from the same country.\n\nPassages:\n\n[King Charles (musician)]\nKing Charles (born Charles Costa, 6 May 1985) is a singer-songwriter from West London.\n\n[Matt Miller (musician)]\nMatt Miller is a native of El Paso, Texas and the bassist for the Post-hardcore band, Sparta.\n\n[Sparta (band)]\nSparta is an American rock band from El Paso, Texas, formed in 2001.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q454c722662",
  "kind": "yes/no",
  "text": "Claim: The poet who wrote Une Tempete and first performed it in Tunisia is French.\n\nPassages:\n\n[Aimé Césaire]\nAimé Fernand David Césaire (26 June 1913 – 17 April 2008) was a Francophone and French poet, author and politician from Martinique. He wrote such works as \"Une Tempête\", a response to Shakespeare's play \"The Tempest\", and \"Discours sur le colonialisme\" (\"Discourse on Colonialism\"), an essay describing the strife between the colonizers and the colonized.\n\n[Une Tempête]\nUne Tempête (\"A tempest\") is a 1969 play by Aimé Césaire. The play was first performed at the Festival d'Hammamet in Tunisia under the direction of Jean-Marie Serreau.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 }
]
