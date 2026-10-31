# A46 replay label-noise blind read RSBS03-blind_read-330ac73d-006

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS03-blind_read-330ac73d-006.json

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
  "qid": "q75cf32963c",
  "kind": "yes/no",
  "text": "Claim: The star of The Big Year acted in a film with martial arts expert Tom Wu. He also voiced Lightning McQueen in the \"Cars\" franchise.\n\nPassages:\n\n[Shanghai Knights]\nDirected by David Dobkin and written by Alfred Gough and Miles Millar, it stars Jackie Chan and Owen Wilson.\n\n[The Big Year]\nThe Big Year is a 2011 American comedy film directed by David Frankel, written by Howard Franklin and starring Jack Black, Steve Martin, and Owen Wilson.\n\n[Tom Wu]\nHe is a martial arts expert who has appeared in films such as \"Revolver\", \"Shanghai Knights\", \"Batman Begins\" and the Bollywood sci-fi movie \"Ra.One\".\n\n[Owen Wilson]\nHe starred with Ben Stiller in numerous films, and is known for his roles in Frat Pack comedies and as well as voicing Lightning McQueen in the \"Cars\" franchise.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qbb9d537019",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Headaches that last all day nonstop🥰😍",
   "I hate headaches and I have one."
  ]
 },
 {
  "qid": "qb55e2c7068",
  "kind": "yes/no",
  "text": "Claim: The second largest convention center on its opening in 1990 is owned by Las Vegas Sands Corporation.\n\nPassages:\n\n[The Palazzo]\nThe hotel and casino are part of a larger complex (operated as one hotel) comprising the adjoining Venetian Resort and Casino and the Sands Convention Center, all of which are owned and operated by the Las Vegas Sands Corporation.\n\n[Sands Expo]\nIt opened in 1990 across the street from the original Sands Hotel, was the second largest convention center in the world when it opened.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q96b4c5d5a7",
  "kind": "yes/no",
  "text": "Claim: The American who owned a piece of land died in May 1999. This piece of land was once owned by Count de Mauny Talvande.\n\nPassages:\n\n[Taprobane Island]\nThe islet passed on to the American author and composer Paul Bowles and then the Sri Lankan born former UN Chief Prosecutor Sir Desmond Lorenz de Silva before it came to the ownership of the Australian businessman Geoffrey Dobbs.\n\n[Count de Mauny]\nMaurice Talvande, Count de Mauny Talvande (self styled), (1866–1941) was a French-born naturalised British landscaper, furniture-maker, and self-inventor, who is best known as the owner and recreator of Taprobane Island, in Sri Lanka.\n\n[Paul Bowles]\nPaul Frederic Bowles ( ; December 30, 1910November 18, 1999) was an American expatriate composer, author, and translator.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q0791571fe0",
  "kind": "yes/no",
  "text": "Claim: Vishal Bhardwaj is the 1965-born field director who directed this 2002 Indian comedy horror film, in which English actor Shweta Basu Prasad won the National Film Award for Best Child Actor.\n\nPassages:\n\n[Makdee]\nMakdee (English: Spider ), promoted as The Web Of The Witch, in English, is a 2002 Indian comedy horror film directed by Vishal Bhardwaj.\n\n[Shweta Basu Prasad]\nFor her performance in the 2002 film Makdee, she won the National Film Award for Best Child Actor.\n\n[Vishal Bhardwaj]\nVishal Bhardwaj (born 4 August 1965) is an Indian film director, screenwriter, producer, music composer and playback singer.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q2b358df9b5",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I reckon I could have put that in the net Morelos sir",
   "That goal should have been easy for Morelos!"
  ]
 },
 {
  "qid": "q8e6df35131",
  "kind": "yes/no",
  "text": "Post: Anyone else remember Twix Tops and M&amp;M's Biscuits or is that just me??",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q98cd77414f",
  "kind": "yes/no",
  "text": "Claim: Kevin Quinn starred in a Disney channel series which was a spinoff of the Jessie show.\n\nPassages:\n\n[Kevin Quinn (actor)]\nHe is known for his starring role in the Disney Channel original series \"Bunk'd\", and his supporting role in the 2016 Disney Channel Original Movie \"Adventures in Babysitting\".\n\n[Bunk'd]\nThe series is a spinoff of \"Jessie\" and stars Peyton List, Karan Brar, Skai Jackson, Miranda May, Kevin Quinn, Nathan Arenas, and Nina Lu.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q0aa5654b25",
  "kind": "yes/no",
  "text": "Claim: Evil controllers was featured on Game informer who was published by the monthly video magazine corporation GameStop Corp.\n\nPassages:\n\n[Evil Controllers]\nEvil Controllers has been featured on majoring gaming sites such as IGN, Kotaku and Game Informer for their Controller Creator that allows shoppers to make fully custom controllers.\n\n[Game Informer]\nThe publication is owned and published by GameStop Corp., the parent company of the video game retailer of the same name, who bought FuncoLand in 2000.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q339ede083b",
  "kind": "yes/no",
  "text": "Claim: The 290m building that features on the list of tallest buildings in Singapore, replaced One Raffles Place, finished in 1986, as the tallest building in Singapore.\n\nPassages:\n\n[Tanjong Pagar Centre]\nWith a height of 290 m , it is currently the tallest building in Singapore, breaking the record held jointly by UOB Plaza, One Raffles Place and Republic Plaza for over 20 years.\n\n[List of tallest buildings in Singapore]\nTanjong Pagar Centre currently holds the title of tallest building in Singapore.\n\n[One Raffles Place]\nAt 280 m , it was also the tallest building in the world outside North America at the time of its completion in 1986, surpassing South Korea's 63 Building completed one year earlier, until it was succeeded by the Bank of China Tower.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qc1e33579a2",
  "kind": "yes/no",
  "text": "Claim: This individual founded Ameche's Drive-in. He and the Wisconsin Badgers player won a Badgers trophy and was elected to the bowl game that also Chris Johnson (running back) has been three times in each of their first four seasons.\n\nPassages:\n\n[Ameche's Drive-in]\nAmeche's Drive-in was a fast-food restaurant chain based in Baltimore, Maryland, founded by Heisman Trophy winner and Baltimore Colts running back Alan Ameche.\n\n[Wisconsin Badgers football]\nWisconsin has had two Heisman Trophy winners, Alan Ameche and Ron Dayne, and have had nine former players inducted into the College Football Hall of Fame.\n\n[Chris Johnson (running back)]\nHe has been to three Pro Bowls and was the NFL's Offensive Player of the Year in 2009.\n\n[Alan Ameche]\nAmeche was elected to the Pro Bowl in each of his first four seasons in the league.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q5eb8094133",
  "kind": "yes/no",
  "text": "Text: You know what works better than therapy? Watching Mamma Mia",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q3dc1565338",
  "kind": "yes/no",
  "text": "Claim: The Highway that connects the major metropolitan areas of St. Louis, Louisville and Lexington in Kentucky, Charleston, West Virginia, and Richmond, Virginia opened in 1975.\n\nPassages:\n\n[Grayson, Kentucky]\nThe city has grown in size substantially since the opening of Interstate 64 in 1975 through Carter County.\n\n[Interstate 64]\nI-64 connects the major metropolitan areas of St. Louis, Louisville and Lexington in Kentucky, Charleston, West Virginia, and Richmond, Virginia.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa867703c88",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "What a wonderful time to have your AC go out https://t.co/jqjqG1dGOa",
   "Literally the worst possible time to have my AC go out."
  ]
 },
 {
  "qid": "qb072303aeb",
  "kind": "yes/no",
  "text": "Claim: The Vines' frontman wrote the song \"Get Free\". He and a special guest performer on If I Loved You: Gentlemen Prefer Broadway are not both from the same country.\n\nPassages:\n\n[Get Free]\nThe song was written by Vines' frontman Craig Nicholls.\n\n[Craig Nicholls]\nCraig Robert Nicholls (born 31 August 1977) is an Australian musician, best known as the lead singer, songwriter, and guitarist of the Australian alternative rock band The Vines, of which he is the only mainstay member.\n\n[If I Loved You: Gentlemen Prefer Broadway]\nThe concert featured men singing classic love songs to one another, and included a full orchestra and performances by Wainwright and special guests Boy George, David Byrne, Josh Groban and Steven Page.\n\n[Boy George]\nBoy George (born George Alan O'Dowd; 14 June 1961) is an English singer, songwriter, DJ, fashion designer and photographer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q8d48acc2c8",
  "kind": "yes/no",
  "text": "Claim: Bassbariton had the lowest vocal range in the group that produced the album Pa un par.\n\nPassages:\n\n[Bass (voice type)]\nA bass ( ) is a type of classical male singing voice and has the lowest vocal range of all voice types.\n\n[Cosmos (band)]\nCosmos was a Latvian a cappella band that formed in Riga in 2002. The band comprised singers Jānis Šipkēvics, Andris Sējāns (both countertenors), Juris Lisenko (tenor), Jānis Ozols (baritone), Jānis Strazdiņš (bass) and Reinis Sējāns (rhythm).\n\n[Pa un par]\nPa un par (On and About) is an album by the Latvian A cappella vocal group Cosmos, that was released on the UPE record label in 2005.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qd912b62922",
  "kind": "yes/no",
  "text": "Claim: Kodaline was formed in a country closer to England than the band that this singer was in from December 1994 until 2007. Galactik Fiestamatik was the second album of this singer.\n\nPassages:\n\n[Rivermaya]\nRivermaya is a Filipino rock band.\n\n[Galactik Fiestamatik]\nGalactik Fiestamatik is the second studio album of Filipino singer, Rico Blanco.\n\n[Kodaline]\nKodaline ( ) are an Irish band.\n\n[Rico Blanco]\nHe began his career as one of the founding members, and served as the chief songwriter, vocalist, guitarist, and keyboardist of the Filipino rock band Rivermaya from 1994 until 2007, and has been a solo artist since 2008.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q682d01a132",
  "kind": "yes/no",
  "text": "Claim: The film The Omega Man featured an actress prior to the release of the 1982 television movie that was shot at Old Ship African Methodist Episcopal Zion Church. This actress featured in the film \"The Monkey Hustle\".\n\nPassages:\n\n[The Monkey Hustle]\nCo-stars include Thomas Carter, Donn C. Harper, Rudy Ray Moore, and Rosalind Cash.\n\n[Old Ship African Methodist Episcopal Zion Church]\nScenes from the 1982 television movie, \"Sister, Sister\", were shot at the church.\n\n[Sister, Sister (1982 film)]\nSister, Sister is a 1982 American drama television movie that stars Diahann Carroll, Rosalind Cash, and Irene Cara.\n\n[Rosalind Cash]\nHer best known film role is as Charlton Heston's character's love interest Lisa, in the 1971 science fiction film, \"The Omega Man\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qae901b7c8c",
  "kind": "yes/no",
  "text": "Claim: The author of and H. L. Mencken were both known for being satirists.\n\nPassages:\n\n[Mythago Wood]\nMythago Wood is a fantasy novel by British writer Robert Holdstock, published in the United Kingdom in 1984.\n\n[Robert Holdstock]\nRobert Paul Holdstock (2 August 1948 – 29 November 2009) was an English novelist and author best known for his works of Celtic, Nordic, Gothic and Pictish fantasy literature, predominantly in the fantasy subgenre of mythic fiction.\n\n[H. L. Mencken]\nHenry Louis Mencken (September 12, 1880 – January 29, 1956) was an American journalist, satirist, cultural critic and scholar of American English.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe0ca826a15",
  "kind": "yes/no",
  "text": "Tweet: @FeeyaCruz Ahahahaha the Feeya I know and love, miss u 😢",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q1a13204a97",
  "kind": "yes/no",
  "text": "Claim: Fredric March costarred in 1935 Australian drama film that Frances Drake is best know for, with the husband of Elsa Lanchester.\n\nPassages:\n\n[Les Misérables (1935 film)]\nLes Misérables is a 1935 American drama film starring Fredric March and Charles Laughton based upon the famous Victor Hugo novel of the same name.\n\n[Charles Laughton]\nIn 1927, he was cast in a play with his future wife Elsa Lanchester, with whom he lived and worked until his death; they had no children.\n\n[Frances Drake]\nFrances Drake (October 22, 1912 – January 18, 2000) was an American actress, best known for playing Eponine in \"Les Misérables\" (1935).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4e30b65164",
  "kind": "yes/no",
  "text": "Claim: Manfred Moch was the featured solo trumpet player of the orchestra named after Bert Kaempfert, the German orchestra leader, music producer, and songwriter born in 1898 and who died on June 21, 1980.\n\nPassages:\n\n[Bert Kaempfert]\nBerthold Heinrich Kämpfert, (16 October 1923 – 21 June 1980), better known as Bert Kaempfert, was a German orchestra leader, music producer, and songwriter.\n\n[Manfred Moch]\nHe made a name for himself in the 1960s as the featured solo trumpet player for the Bert Kaempfert orchestra, contributing memorable and melodic solos to many of Kaempfert’s hits; such songs included “Bye Bye Blues”, “Strangers In The Night”, “L-O-V-E” and “Sweet Maria”.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf231847436",
  "kind": "yes/no",
  "text": "Claim: Besides the song of the same name as Radiohead's album that Radiodread is a cover of, the same band also recorded \"Lucky\" in 1995.\n\nPassages:\n\n[OK Computer]\nOther than the song \"Lucky\", which was recorded in 1995, Radiohead recorded the album in Oxfordshire and Bath between 1996 and early 1997, mostly in the historic mansion St Catherine's Court.\n\n[No Surprises]\n\"No Surprises\" is a song by the English alternative rock band Radiohead, released as the third and final single from their third studio album \"OK Computer\" (1997) on 12 January 1998.\n\n[Radiodread]\nRadiodread is a 2006 tribute album by the Easy Star All-Stars that covers Radiohead's 1997 album \"OK Computer\" in reggae, ska and dub styles.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q99b0a6dc39",
  "kind": "yes/no",
  "text": "Claim: Jack Harvey was born in a small civil parish that as of 2011 had a population of 1,425.\n\nPassages:\n\n[Bassingham]\nBassingham is a village and civil parish in the North Kesteven district of Lincolnshire, England. The population of the civil parish at the 2011 census was 1,425.\n\n[Jack Harvey (racing driver)]\nJack Harvey (born 15 April 1993 in Bassingham, Lincolnshire) is a British auto racing driver, and a former member of McLaren's Young Driver Programme.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa811439536",
  "kind": "yes/no",
  "text": "Claim: Soletrader Peek A Boo is of this long-haired breed. It and Toy Trawler Spaniel are both breeds of dog.\n\nPassages:\n\n[Soletrader Peek A Boo]\nSoletrader Peek A Boo, also known as Jilly, is a Petit Basset Griffon Vendéen show dog owned by Sara Robertson and Wendy Doherty and handled by Gavin Robertson, who won Best in Show at Crufts in 2013.\n\n[Petit Basset Griffon Vendéen]\nThe Petit Basset Griffon Vendéen ( ), or PBGV, is a breed of dog of the scent hound type, bred to trail hares in bramble-filled terrain of the Vendée district of France.\n\n[Toy Trawler Spaniel]\nThe Toy Trawler Spaniel is an extinct breed of Spaniel which physically was similar to the King Charles Spaniel of the 16th century.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q35a2debe90",
  "kind": "yes/no",
  "text": "Claim: The auditorium where Backstreet Boys: Larger Than Life residency show perfomed at is located in the Planet Hollywood Resort & Casino in Las Vegas, Nevada. This auditorium is located at a hotel and casino owned by Caesars Entertainment Corporation.\n\nPassages:\n\n[The AXIS]\nThe AXIS (known as The AXIS powered by Monster for sponsorship purposes, also referred to as the AXIS Theater) is a mid-sized auditorium located at Planet Hollywood Las Vegas on the Las Vegas Strip.\n\n[Backstreet Boys: Larger Than Life]\nBackstreet Boys: Larger Than Life is the first residency show by American vocal group Backstreet Boys, performed at The AXIS auditorium located in the Planet Hollywood Resort & Casino in Las Vegas, Nevada.\n\n[Planet Hollywood Las Vegas]\nIt is owned and operated by Caesars Entertainment Corporation.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q5ba0de7edc",
  "kind": "yes/no",
  "text": "Claim: Mel Duncan holds a history degree from the private, coeducational liberal arts Macalester College located in Saint Paul, Minnesota, US.\n\nPassages:\n\n[Mel Duncan]\nMelvin Earl Duncan (born May 22, 1950 in Davenport, Iowa) is the founding Executive Director of Nonviolent Peaceforce (NP), a civilian peacekeeping organization based in Brussels. He holds a bachelor's degree in Political Science from Macalester College in St. Paul, Minnesota and a Master of Arts in Humanities and Leadership from New College of California.\n\n[Macalester College]\nMacalester College ( ) is a private, coeducational liberal arts college located in Saint Paul, Minnesota, US.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5cb8479533",
  "kind": "yes/no",
  "text": "Claim: Fash Mosque is 4.5 km away from the mosque where Ayyub was Imam, which was originally built. It was built by the prophet the Islamic Information Center provides religious information on.\n\nPassages:\n\n[Fas'h mosque]\nIt is 4.5 km from Al-Masjid an-Nabawi.\n\n[Al-Masjid an-Nabawi]\nAl-Masjid an-Nabawī (Arabic: ٱلْمَسْجِدُ ٱلنَّبَويّ‎ , 'Prophet's Mosque' ‎ ) is a mosque established and originally built by the Islamic prophet Muhammad, situated in the city of Medina in Saudi Arabia.\n\n[Islamic Information Center]\nThe main purpose of this organization is to provide authentic Islamic information as taught by the Islamic prophet Muhammad and his descendants.\n\n[Muhammad Ayyub]\nHe was an Imam of Al-Masjid an-Nabawi in Medina, Saudi Arabia.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q827d19f0ad",
  "kind": "yes/no",
  "text": "Claim: Multinational Monitor has more issues each month than In These Times does.\n\nPassages:\n\n[Multinational Monitor]\nThe Multinational Monitor was a bimonthly magazine founded by Ralph Nader in 1980.\n\n[In These Times]\nIn These Times is an American politically progressive/democratic socialist monthly magazine of news and opinion published in Chicago, Illinois.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q7e86013a4f",
  "kind": "yes/no",
  "text": "Claim: Priceline.com is a company in the discount travel market. The company which acquired the company that produced Red Tails in 2012 is not in the discount travel market.\n\nPassages:\n\n[Lucasfilm]\nThe Walt Disney Company acquired Lucasfilm in 2012 at a valuation of $4.06 billion.\n\n[Red Tails]\nThis was Cuba Gooding Jr.'s first theatrically released film in five years since his starring role in 2007's \"Daddy Day Camp\".\n\n[Priceline.com]\nPriceline.com is an American company and a commercial website that helps users find discount rates for travel-related purchases such as airline tickets and hotel stays.\n\n[The Walt Disney Company]\nThe Walt Disney Company, commonly known as Disney, is an American diversified multinational mass media and entertainment conglomerate, headquartered at the Walt Disney Studios in Burbank, California.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q52da84c2b0",
  "kind": "yes/no",
  "text": "Claim: More than 1,600 German scientists, engineers, and technicians, were recruited in post-Nazi Germany as a result of the clandestine operation where Arthur Rudolph became one of the main developers of the 1960s U.S. space program.\n\nPassages:\n\n[Arthur Rudolph]\nAfter the war, the United States Government's Office of Strategic Services (OSS) brought him to the U.S. as part of the clandestine Operation Paperclip, where he became one of the main developers of the U.S. space program.\n\n[Operation Paperclip]\nOperation Paperclip was a secret program of the Joint Intelligence Objectives Agency (JIOA) in which more than 1,600 German scientists, engineers, and technicians, such as Wernher von Braun and his V-2 rocket team, were recruited in post-Nazi Germany and taken to the U.S. for government employment, at the end of World War II; many were members and some were leaders of the Nazi Party.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3dbdcd30e3",
  "kind": "yes/no",
  "text": "Tweet: You’re all sickos for being mean to Trump so much for the tolerant left 🙄\n\nanyways George Floyd had it coming",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q8b6ee499ba",
  "kind": "yes/no",
  "text": "Claim: The album that the song Juntos (Together) is on is not a sports film. The 1979 show Peter Ellenshaw made before retiring is also not a sports film.\n\nPassages:\n\n[Peter Ellenshaw]\nHe retired after his work on \"The Black Hole\" (1979), but contributed matte paintings for \"Dick Tracy\" (1990).\n\n[The Black Hole]\nThe Black Hole is a 1979 American science fiction film directed by Gary Nelson and produced by Walt Disney Productions.\n\n[Juntos (Together)]\nThe song was released digitally via the iTunes Store by Walt Disney Records and Universal Music Latin on January 20, 2015, as the lead single from the soundtrack for \"McFarland, USA\".\n\n[McFarland, USA]\nMcFarland, USA (also known as McFarland) is a 2015 American sports drama film directed by Niki Caro, produced by Mark Ciardi and Gordon Gray, written by Christopher Cleveland, Bettina Gilois and Grant Thompson with music composed by Antônio Pinto.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q208cf0cc78",
  "kind": "yes/no",
  "text": "Claim: The 2015 Austrian thriller film Jack tells the story of a serial killer who died in 1994.\n\nPassages:\n\n[Jack Unterweger]\nJohann \"Jack\" Unterweger (16 August 195029 June 1994) was an Austrian serial killer who murdered prostitutes in several countries.\n\n[Jack (2015 film)]\nJack is a 2015 Austrian thriller film about serial killer Jack Unterweger, directed by Elisabeth Scharang.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qf00bb52850",
  "kind": "yes/no",
  "text": "Claim: The Greene County representative of a narrow pass through the mountains belongs to the Republican party.\n\nPassages:\n\n[Cumberland Gap]\nThe Cumberland Gap is a narrow pass through the long ridge of the Cumberland Mountains, within the Appalachian Mountains, near the junction of the U.S. states of Kentucky, Virginia, and Tennessee.\n\n[Terry Kilgore]\nA Republican, he was elected to the Virginia House of Delegates in 1993, and became chair of the Commerce and Labor committee in 2008.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q0b3ee7fe99",
  "kind": "yes/no",
  "text": "Claim: Marion is approximately 50 miles north of L.A. which is the third-most populous state capital in the U.S.\n\nPassages:\n\n[Marion, Ohio]\nMarion is a city in and the county seat of Marion County, Ohio, United States.\n\n[Columbus, Ohio]\nColumbus ( ) is the capital and largest city of the U.S. state of Ohio. This makes Columbus the third-most populous state capital in the United States, and the second-largest city in the Midwestern United States, after Chicago.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q782ce312e9",
  "kind": "yes/no",
  "text": "Claim: The author of Varieties of Disturbance wrote shorter works than Raymond Carver.\n\nPassages:\n\n[Varieties of Disturbance]\nVarieties of Disturbance is Lydia Davis's fourth collection of short stories.\n\n[Raymond Carver]\nRaymond Clevie Carver Jr. (May 25, 1938 – August 2, 1988) was an American short-story writer and poet. Carver contributed to the revitalization of the American short story during the 1980s.\n\n[Lydia Davis]\nLydia Davis (born July 15, 1947) is an American writer noted for literary works of extreme brevity (commonly called \"flash fiction\").",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe2dd1ad638",
  "kind": "yes/no",
  "text": "Claim: The genus which use the flowering species Endoclita excrescens as a food plant contains a larger variety of species than the genus Dendromecon. Other food plants include Castanea\", \"Nicotiana\", \"Quercus\", and \"Raphanus\".\n\nPassages:\n\n[Paulownia]\nPaulownia is a genus of six to 17 species (depending on taxonomic authority) of flowering plants in the family Paulowniaceae, related to and sometimes included in the Scrophulariaceae.\n\n[Dendromecon]\nDendromecon, the tree poppy, is a genus of one or two species of shrubs to small trees, native to California and northern Baja California.\n\n[Endoclita excrescens]\nFood plants for this species include \"Castanea\", \"Nicotiana\", \"Paulownia\", \"Quercus\", and \"Raphanus\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe41172774c",
  "kind": "yes/no",
  "text": "Claim: The SS-owned company that funded a Nazi association to raise the birth rate of \"Aryan\" children was created in 1942 to market a reflector invented by the chauffeur of Hitler.\n\nPassages:\n\n[Anton Loibl GmbH]\nAnton Loibl GmbH was a company owned by the SS which was a funding source for the Ahnenerbe research branch and the Lebensborn eugenics programme. It was created to market a bicycle reflector invented by Anton Loibl, a chauffeur for Hitler.\n\n[Lebensborn]\nLebensborn e.V. (literally: \"Fount of Life\") was an SS-initiated, state-supported, registered association in Nazi Germany with the goal of raising the birth rate of \"Aryan\" children of persons classified as \"racially pure and healthy\" based on Nazi racial hygiene and health ideology.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2e1ea3148c",
  "kind": "yes/no",
  "text": "Claim: The football club that formed in 1876 and has Dael Jonathan Fry as a player is Middlesbrough.\n\nPassages:\n\n[Middlesbrough F.C.]\nFormed in 1876, they have played at the Riverside Stadium since 1995, their third ground since turning professional in 1889.\n\n[Dael Fry]\nDael Jonathan Fry (born 30 August 1997) is an English professional footballer who plays as a centre back for EFL Championship club Middlesbrough.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q35a9336af6",
  "kind": "yes/no",
  "text": "Claim: The documentaries, The Mosuo Sisters, and Quantum Hoops, were not both released in the same year.\n\nPassages:\n\n[Quantum Hoops]\nQuantum Hoops is a 2007 documentary film directed by Rick Greenwald, that follows the California Institute of Technology's basketball team—the Caltech Beavers—in their attempts to end a 21-year losing streak during the final week of the 2006 basketball season.\n\n[The Mosuo Sisters]\nThe Mosuo Sisters is a 2012 documentary film written and directed by Marlo Poras.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q869554ed7e",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "@SkySportsBoxing if i think you would have a chance against fury i mean its easy for some broken bodied old boy to beat the best in the world",
   "Haye as a competitive fight against fury which is a 50-50 fight and could go either way"
  ]
 },
 {
  "qid": "q32546e644a",
  "kind": "yes/no",
  "text": "Claim: Louis Leterrier is a French film director whose films include the first two \"Transporter\" films. The Transporter is an English-language French action thriller film directed by Corey Yuen and Louis Leterrier, released in 2002.\n\nPassages:\n\n[The Transporter]\nThe Transporter (French: Le Transporteur) is a 2002 English-language French action thriller film directed by Corey Yuen and Louis Leterrier (who is credited as artistic director on the project), and written by Luc Besson, who was inspired by BMW Films' \"The Hire\" series.\n\n[Louis Leterrier]\nLouis Leterrier (born June 17, 1973) is a French film director whose films include the first two \"Transporter\" films, \"Unleashed\" (2005), \"The Incredible Hulk\" (2008), \"Clash of the Titans\" (2010) and \"Now You See Me\" (2013).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q04dfa21aaf",
  "kind": "yes/no",
  "text": "Claim: The Neoclassical monument Benito Juárez Hemicycle is located in this city of Mexico that consists of sixteen municipalities.\n\nPassages:\n\n[Benito Juárez Hemicycle]\nThe Benito Juárez Hemicycle is a Neoclassical monument located at the Alameda Central park in Mexico City, Mexico and commemorating the Mexican statesman Benito Juárez.\n\n[Mexico City]\nThe city consists of sixteen municipalities.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q81cb1fa073",
  "kind": "yes/no",
  "text": "Claim: Timothy Simon \"Tim\" Roth no obtuvo reconocimiento antes que la madre de Nat y Alex Wolffs.\n\nPassages:\n\n[Nat and Alex Wolff]\nThe siblings are known for their work on the Nickelodeon television series \"The Naked Brothers Band\", which was created and produced by their mother, actress Polly Draper.\n\n[Polly Draper]\nShe first gained recognition for her role in the ABC primetime television drama \"Thirtysomething\" (1987–91).\n\n[Tim Roth]\nTimothy Simon \"Tim\" Roth (born 14 May 1961) is an English actor and director. He garnered critical acclaim for his role as Myron in the 1984 film \"The Hit\" (1984), for which he was nominated for his first BAFTA Award.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q858c64a61a",
  "kind": "yes/no",
  "text": "Claim: An American pharmacist was inspired to invent cola due to a coca wine recipe from Angelo Mariani.\n\nPassages:\n\n[Cola]\nColas became popular worldwide after pharmacist John Pemberton invented Coca-Cola in 1886. His non-alcoholic recipe was inspired by the coca wine of pharmacist Angelo Mariani, created in 1863.\n\n[John Pemberton]\nJohn Stith Pemberton (July 8, 1831 – August 16, 1888) was an American pharmacist, and is best known for being the founder of Coca-Cola.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qe02f9e9f37",
  "kind": "yes/no",
  "text": "Post: There is not enough people here #ivoryrooms",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qf0212a8993",
  "kind": "yes/no",
  "text": "Claim: François-Jean Pelletier worked in politics in Silver Bow County in Nevada in which their county seat is Butte.\n\nPassages:\n\n[François Jean Pelletier]\nPelletier was elected to the Legislature of the State of Montana for Silver Bow County in 1899 and 1901.\n\n[Silver Bow County, Montana]\nSilver Bow County is a county in the State of Montana. Its county seat is Butte.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q66590355d5",
  "kind": "yes/no",
  "text": "Claim: A Pair of Brown Eyes and Wild Mountain Thyme is based from the artist Francis McPeake's song.\n\nPassages:\n\n[A Pair of Brown Eyes]\nIt featured on the band's second album, \"Rum Sodomy & the Lash\", and was composed by Pogues front man Shane MacGowan, on the melody of \"Wild Mountain Thyme\", also known as \"Will Ye Go Lassie Go,\" a song by Francis McPeake in a traditional Irish folk style.\n\n[Wild Mountain Thyme]\nis a Scottish folk song that was collected by Francis McPeake 1st, who wrote the song himself for his wife.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q18bc7ba92a",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "Young people are in need of the stimulus too. Just because we do not have kids does not mean that we do not have bills, debt, etc.",
   "Stimulus checks should come with hand lotion, a face mask, and a bonus for every Instagram bingos you do"
  ]
 }
]
