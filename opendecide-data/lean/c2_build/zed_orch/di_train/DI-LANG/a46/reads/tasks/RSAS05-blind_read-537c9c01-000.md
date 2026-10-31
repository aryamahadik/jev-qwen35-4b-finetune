# A46 replay label-noise blind read RSAS05-blind_read-537c9c01-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS05-blind_read-537c9c01-000.json

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
  "qid": "q70c030a8e9",
  "kind": "yes/no",
  "text": "Claim: World UFO Day is celebrated on the day an American aviator claimed to see nine hot dog shapped objects flying near Mount Rainier, Washington.\n\nPassages:\n\n[World UFO Day]\nJune 24 is the date that aviator Kenneth Arnold reported what is generally considered to be the first widely reported unidentified flying object sighting in the United States, while July 2 commemorates the supposed UFO crash in the 1947 Roswell UFO Incident.\n\n[Kenneth Arnold]\nHe is best known for making what is generally considered the first widely reported unidentified flying object sighting in the United States, after claiming to have seen nine unusual objects flying in tandem near Mount Rainier, Washington on June 24, 1947.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qbb3a07a17b",
  "kind": "yes/no",
  "text": "Claim: The population of the largest city in Trego County is 1,862.\n\nPassages:\n\n[WaKeeney, Kansas]\nAs of the 2010 census, the city population was 1,862.\n\n[Trego County, Kansas]\nIts county seat and largest city is WaKeeney.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1945286ed3",
  "kind": "yes/no",
  "text": "Claim: The Magic Roundabout is a 2005 French-British, computer-animated, adventure fantasy film based on the comedic television series The Magic Roundabout.\n\nPassages:\n\n[Ray Winstone]\nHe has also become well known as a voice over actor, and has recently branched out into film production.\n\n[The Magic Roundabout (film)]\nThe Magic Roundabout (released in France as Pollux - Le manège enchanté and redubbed in the United States as Doogal or The Lord of the Springs) is a 2005 French-British computer-animated adventure fantasy film based on the television series \"The Magic Roundabout\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q11961c48e8",
  "kind": "yes/no",
  "text": "Claim: The actor star of the film \"Five Easy Pieces\" played a Teamsters leader in a 1992 French-American biographical crime film directed by Robert Ciaro.\n\nPassages:\n\n[Jack Nicholson]\nJohn Joseph Nicholson (born April 22, 1937) is an American actor and filmmaker, who has performed for over 60 years.\n\n[Hoffa]\nHoffa is a 1992 French-American biographical crime film directed by Danny DeVito and written by David Mamet, based on the life of Teamsters leader Jimmy Hoffa. Jack Nicholson plays Hoffa, and DeVito plays Robert Ciaro, an amalgamation of several Hoffa associates over the years.\n\n[Five Easy Pieces]\nThe film stars Jack Nicholson, with Karen Black, Susan Anspach, Ralph Waite, and Sally Struthers in supporting roles.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q15130f46a5",
  "kind": "yes/no",
  "text": "Claim: Four runway RAF Skellingthorpe was operational during the war that lasted from 1939 to 1945.\n\nPassages:\n\n[RAF Skellingthorpe]\nRoyal Air Force Skellingthorpe or more simply RAF Skellingthorpe is a former Royal Air Force station which was operational during the Second World War.\n\n[World War II]\nWorld War II (often abbreviated to WWII or WW2), also known as the Second World War, was a global war that lasted from 1939 to 1945, although related conflicts began earlier.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4dfbc9b3a3",
  "kind": "yes/no",
  "text": "Claim: The author of Bambi's Children: The Story of a Forest Family, originally titled his work Bambi: Eine Lebensgeschichte aus dem Walde.\n\nPassages:\n\n[Felix Salten]\nFelix Salten (6 September 1869 – 8 October 1945) was an Austrian author and critic in Vienna.\n\n[Bambi, a Life in the Woods]\nBambi, a Life in the Woods, originally published in Austria as Bambi: Eine Lebensgeschichte aus dem Walde is a 1923 Austrian novel written by Felix Salten and published by Ullstein Verlag.\n\n[Bambi's Children]\nBambi's Children: The Story of a Forest Family (German: Bambis Kinder: Eine Familie im Walde ) is a novel written by Austrian author Felix Salten as a sequel to his successful work \"Bambi, A Life in the Woods\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qc40fd62d09",
  "kind": "yes/no",
  "text": "Claim: Mervyn Leroy was a music producer. The writer and director of Surviving Desire was also a producer.\n\nPassages:\n\n[Hal Hartley]\nHal Hartley (born November 3, 1959) is an American film director, screenwriter, producer and composer who became a key figure in the American independent film movement of the 1980s and '90s.\n\n[Mervyn LeRoy]\nMervyn LeRoy (October 15, 1900 – September 13, 1987) was an American film director, film producer and occasional actor.\n\n[Surviving Desire]\nSurviving Desire is a 1991 American comedy-drama film written and directed by Hal Hartley.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q6d476b667e",
  "kind": "yes/no",
  "text": "Post: i cant wait to like get my own place and get a lil cat someday im allergic to cats but its Ok",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q5d6f4df773",
  "kind": "yes/no",
  "text": "Text: my hobbies include leaving projects for the night before and then complaining that the teacher didn't give us enough time 🙃🙃",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q90bf2a1bad",
  "kind": "yes/no",
  "text": "Claim: The bassist in a band is the cousin of the lead singer of Saint Asonia. This lead vocalist and Björk are both singers. This band released an album Vices and Virtues.\n\nPassages:\n\n[Vices and Virtues (Art of Dying album)]\nVices and Virtues is the second studio album by Canadian rock band Art of Dying.\n\n[Björk]\nBjörk Guðmundsdóttir (] , born 21 November 1965), known as Björk ( ), is an Icelandic singer, songwriter, actress, record producer, and DJ.\n\n[Art of Dying (band)]\nBassist Cale Gontier is the cousin of Adam Gontier, the lead singer of Saint Asonia and former lead singer of Three Days Grace.\n\n[Adam Gontier]\nAdam Wade Gontier (born May 25, 1978) is a Canadian singer, songwriter and musician.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q592c6f7cfb",
  "kind": "yes/no",
  "text": "Claim: About Time is a British romantic comedy-drama film that stars an Irish actor and writer who recieved a Bachelor of Arts from Dublin Institute of Technology.\n\nPassages:\n\n[About Time (2013 film)]\nAbout Time is a 2013 British romantic comedy-drama film about a young man with the special ability to time travel who tries to change his past in order to improve his future. The film was written and directed by Richard Curtis, and stars Domhnall Gleeson, Rachel McAdams and Bill Nighy.\n\n[Domhnall Gleeson]\nDomhnall Gleeson ( ; born 12 May 1983) is an Irish actor and writer. He received a Bachelor of Arts in Media Arts from Dublin Institute of Technology.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qfac27ad8a4",
  "kind": "yes/no",
  "text": "Claim: The majority of John D. Odegard School of Aerospace Sciences' fleet is based at this facility. This facility is closer to the town it is near, than the airport close by to The Texas Air & Space Museum.\n\nPassages:\n\n[Texas Air &amp; Space Museum]\nThe Texas Air & Space Museum is an aviation museum located near Rick Husband Amarillo International Airport in Amarillo, Texas.\n\n[John D. Odegard School of Aerospace Sciences]\nThe majority of the school's fleet of over 120 aircraft is based at nearby Grand Forks International Airport and is the largest fleet of civilian flight training aircraft in North America.\n\n[Grand Forks International Airport]\nGrand Forks International Airport (IATA: GFK, ICAO: KGFK, FAA LID: GFK) is a public airport five miles (8 km) northwest of Grand Forks, in Grand Forks County, North Dakota.\n\n[Rick Husband Amarillo International Airport]\nRick Husband Amarillo International Airport (IATA: AMA, ICAO: KAMA, FAA LID: AMA) is a public airport six miles (10 km) east of downtown Amarillo, in Potter and Randall Counties, Texas, United States.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q1245908dea",
  "kind": "yes/no",
  "text": "Claim: Natalie Martinez is know for her role in the 2008 American-German-British speculative fiction action thriller Death Race.\n\nPassages:\n\n[Natalie Martinez]\nNatalie Martinez (born July 12, 1984) is an American actress and model. She is known as the spokes-model for JLO by Jennifer Lopez, and for her role in the 2008 feature film \"Death Race\".\n\n[Death Race (film)]\nDeath Race is a 2008 American-German-British science fiction action thriller film produced, written, and directed by Paul W. S. Anderson and starring Jason Statham.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qefff2bbb77",
  "kind": "yes/no",
  "text": "Claim: The budget of the 2007 horror film starring Geoffrey Simpson was $60 million. One of the stars from the film also voiced Norman Babcock.\n\nPassages:\n\n[Geoffrey Simpson]\nHe has received critical praise for his work on films including \"Shine\", \"Oscar and Lucinda\" (1997) and \"Romulus, My Father\" (2007).\n\n[ParaNorman]\nThe film mainly received positive reviews and was a modest box office success, earning $107 million against its budget of $60 million.\n\n[Romulus, My Father]\nA film adaptation, \"Romulus, My Father\", was released in 2007, starring Eric Bana, Franka Potente and Kodi Smit-McPhee.\n\n[Kodi Smit-McPhee]\nHe is best known for his roles as The Boy in \"The Road\", Owen in \"Let Me In\", Norman Babcock in \"ParaNorman\", Alexander in \"Dawn of the Planet of the Apes\", and Nightcrawler in the 2016 film \"\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8e1098866e",
  "kind": "yes/no",
  "text": "Text: Damn, imagine being vaxxed and then getting a cold and then losing your taste and smell.\n\nOh wait.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qad82f1d121",
  "kind": "yes/no",
  "text": "Claim: Daniel Hudson Burnham was born before a famous skyscraper architect. That architect designed the Society for Saving Buildings.\n\nPassages:\n\n[Society for Savings Building]\nIt was designed by John Wellborn Root of the Chicago-based architectural firm Burnham & Root.\n\n[Daniel Burnham]\nDaniel Hudson Burnham, FAIA (September 4, 1846 – June 1, 1912) was an American architect and urban designer.\n\n[John Wellborn Root]\nJohn Wellborn Root (January 10, 1850 – January 15, 1891) was an American architect who was based in Chicago with Daniel Burnham.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q03ab04bd21",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "My roommate has no redeeming qualities",
   "I've made a roommate complain tweet every day, and he's done another thing, but I'm tired of negativity so I'm gonna list all the things I like about him! Here they are:"
  ]
 },
 {
  "qid": "q4c3f2b0962",
  "kind": "yes/no",
  "text": "Claim: The species of Spruce is native an area found in eastern North America. This area is located on the geological formation that Round Pond (Berlin, in the state Ricardo Carreras is from) lake is located.\n\nPassages:\n\n[Round Pond (Berlin, New York)]\nThe lake is located on a geologic formation known as the Rensselaer Plateau.\n\n[Picea rubens]\nPicea rubens, commonly known as red spruce, is a species of spruce native to eastern North America, ranging from eastern Quebec to Nova Scotia, and from New England south in the Adirondack Mountains and Appalachians to western North Carolina.\n\n[Ricardo Carreras]\nCarreras was born in New York City, New York.\n\n[Rensselaer Plateau]\nVegetation on the plateau is more similar to that found in the Adirondack Mountains to the northwest, with abundant Eastern White Pine, Eastern Hemlock, Red Spruce, and Balsam Fir, along with more limited occurrences of Red Pine and Tamarack.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q319d30ceb0",
  "kind": "yes/no",
  "text": "Claim: The closest relative to the whale is located in New Zealand.\n\nPassages:\n\n[Hippopotamus]\nThe common hippopotamus (\"Hippopotamus amphibius\"), or hippo, is a large, mostly herbivorous and aggressive mammal in sub-Saharan Africa, and one of only two extant species in the family Hippopotamidae, the other being the pygmy hippopotamus (\"Choeropsis liberiensis\" or \"Hexaprotodon liberiensis\").\n\n[Whale]\nThey are an informal grouping within the infraorder Cetacea, usually excluding dolphins and porpoises. Whales, dolphins and porpoises belong to the order Cetartiodactyla with even-toed ungulates and their closest living relatives are the hippopotamuses, having diverged about 40 million years ago.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qd8d25e293b",
  "kind": "yes/no",
  "text": "Claim: War for the Planet of the Apes is a 2017 American science fiction film directed by Matt Reeves, a sequel to 2014 American science fiction film, Dawn of the Planet of the Apes, directed by Matt Reeves and written by Mark Bomback, Rick Jaffa and Amanda Silver. Both are based on the original series of movies from the 20th Century.\n\nPassages:\n\n[War for the Planet of the Apes]\nA sequel to \"Rise of the Planet of the Apes\" (2011) and \"Dawn of the Planet of the Apes\" (2014), it is the third installment in the \"Planet of the Apes\" reboot series.\n\n[Dawn of the Planet of the Apes]\nDawn of the Planet of the Apes is a 2014 American science fiction film directed by Matt Reeves and written by Mark Bomback, Rick Jaffa and Amanda Silver.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q13d37fffa2",
  "kind": "yes/no",
  "text": "Claim: This 55-year old company operates flights to Lufthansa destinations, on behalf of Lufthansa. Its headquarters are 4 km from the city center.\n\nPassages:\n\n[Lufthansa destinations]\nFlights operated on behalf of Lufthansa by PrivatAir are also listed.\n\n[PrivatAir]\nPrivatAir is a Swiss airline operating business jets, headquartered at Geneva Airport in Meyrin.\n\n[Geneva Airport]\nIt is located 4 km northwest of the city centre.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q84c255b2ec",
  "kind": "yes/no",
  "text": "Claim: The builder of the Hyundai Stellar is located in Seoul.\n\nPassages:\n\n[Hyundai Stellar]\nThe Hyundai Stellar (Hangul: ) was a mid-size rear-wheel drive automobile produced by the Hyundai Motor Company to succeed the soon to be replaced Ford Cortina that Hyundai were building under licence.\n\n[Hyundai Motor Company]\nThe Hyundai Motor Company (Hangul: 현대자동차 ; Hanja: 現代自動車 ; RR: \"Hyeondae Jadongcha \" ; Hangul: 현대 ; Hanja: 現代 ; MR: \"Hyŏndae \" , ] , \"modernity\"; ) is a South Korean multinational automotive manufacturer headquartered in Seoul, South Korea.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q885fd41ce7",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "not to alarm anyone but i just saw spider-man by uta",
   "ALERT, spider-man is on the uta campus."
  ]
 },
 {
  "qid": "qfa790a7ecf",
  "kind": "yes/no",
  "text": "Claim: Mark Chamberlain and Alex Oxlade-Chamberlain were being an English professinal footballer.\n\nPassages:\n\n[Alex Oxlade-Chamberlain]\nAlexander Mark David Oxlade-Chamberlain (born 15 August 1993) is an English professional footballer who plays as a midfielder for Premier League club Liverpool and the England national team.\n\n[Mark Chamberlain]\nMark Valentine Chamberlain (born 19 November 1961) is an English former international footballer. He is the younger brother of Neville Chamberlain, and the father of Liverpool and England international player Alex Oxlade-Chamberlain and Portsmouth's Christian Oxlade-Chamberlain.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q79a9bfdac4",
  "kind": "yes/no",
  "text": "Claim: The olympic wrestler who defeated Elmadi Zhabrailov later went on to coach wrestling at Iowa State University.\n\nPassages:\n\n[Kevin Jackson]\nAfter retiring from active competition he became the head wrestling coach at Iowa State University, having been hired in 2009 after Cael Sanderson moved to Penn State University.\n\n[Elmadi Zhabrailov]\nHis elder brother Lukman prepared him for the 1992 Olympics, where Elmadi won a silver medal, losing the final bout to Kevin Jackson via a controversial decision.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3a76fc90a8",
  "kind": "yes/no",
  "text": "Claim: American Heavy metal band Pantera worked with producer Terry Date and released four albums during the 1980's.\n\nPassages:\n\n[Pantera]\nHaving started as a glam metal band, Pantera released four albums during the 1980s.\n\n[Terry Date]\nTerry Date (born January 31, 1956) is an American record producer and engineer, specializing in the rock genres, especially heavy metal.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q604b2d1978",
  "kind": "yes/no",
  "text": "Tweet: No but the worst type of boy is the one that wears shorts and sandals when it’s snowing and constantly reminds you that it’s not that cold",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qa19da6da86",
  "kind": "yes/no",
  "text": "Claim: The chorus of \"On the Radio\" by Regina Spektor contains references to the love song \"November Rain\" by Guns N' Roses, an American hard rock band.\n\nPassages:\n\n[November Rain]\n\"November Rain\" is a power ballad by the American hard rock band Guns N' Roses.\n\n[On the Radio (Regina Spektor song)]\nThe chorus contains references to the song \"November Rain\" by Guns N' Roses.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q099743d640",
  "kind": "yes/no",
  "text": "Claim: Between the two Oblivians bands, Squirrel Nut Zippers was formed earlier. Singles Collection: 2008–2011 is a box set by Oblivians rock band that was formed after.\n\nPassages:\n\n[Singles Collection: 2008–2011]\nSingles Collection: 2008–2011 is a box set by American rock band The Gaslight Anthem which was released on June 18, 2013.\n\n[Squirrel Nut Zippers]\nThe Squirrel Nut Zippers is an American swing band formed in 1993 in Chapel Hill, North Carolina, by James \"Jimbo\" Mathus (vocals and guitar), Tom Maxwell (vocals and guitar), Katharine Whalen (vocals, banjo, ukulele), Chris Phillips (drums), Don Raleigh (bass guitar), and Ken Mosher.\n\n[The Gaslight Anthem]\nThe Gaslight Anthem is an American rock band from New Brunswick, New Jersey, formed in 2006.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q0497d07387",
  "kind": "yes/no",
  "text": "Claim: A Indo-European linguist, was a member of the Kazan School. This Indo-European linguist was published by Michigan Slavic Publications. This publisher was founded by Ladislav Matejka.\n\nPassages:\n\n[Kazan school]\nKazan School was an influential group of linguists in Kazan. The linguistic circle included the Polish linguist Jan Baudouin de Courtenay and his student Nikolai Trubetzkoy.\n\n[Nikolai Trubetzkoy]\nPrince Nikolai Sergeyevich Trubetzkoy (also Troubetskoy; Russian: Никола́й Серге́евич Трубецко́й; Moscow, April 16, 1890 – Vienna, June 25, 1938) was a Russian linguist and historian whose teachings formed a nucleus of the Prague School of structural linguistics.\n\n[Ladislav Matejka]\nIn 1962, he founded Michigan Slavic Publications, a series that has published more than 100 volumes by authors such as Roman Jakobson and Nikolai Trubetzkoy.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q3e955cae76",
  "kind": "yes/no",
  "text": "Claim: The former college football quarterback Julius Caesar \"J. C.\" Watts Jr. is the nephew Wade Watts.\n\nPassages:\n\n[J. C. Watts]\nJulius Caesar \"J. C.\" Watts Jr. (born November 18, 1957) is an American politician from Oklahoma who was a college football quarterback for the Oklahoma Sooners and later played professionally in the Canadian Football League.\n\n[Wade Watts]\nHe worked with Thurgood Marshall and developed a friendship with Martin Luther King during the American civil rights movement, and has been cited as a mentor by the current leader of the NAACP in Oklahoma, Miller Newman, and his nephew, former congressman, J. C. Watts.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb4a86bb5a8",
  "kind": "yes/no",
  "text": "Claim: Charlton Heston starred in the film The Human Factor in 1979, alongside fellow English actors Richard Attenborough and Derek Jacobi.\n\nPassages:\n\n[The Human Factor (1979 film)]\nThe Human Factor is a 1979 British thriller film starring Richard Attenborough, Nicol Williamson, Derek Jacobi, and John Gielgud.\n\n[Derek Jacobi]\nSir Derek George Jacobi, ( ; born 22 October 1938) is an English actor and stage director.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q24539b34cd",
  "kind": "yes/no",
  "text": "Claim: The rock band that recorded Shapes (album), not The Black Keys, is an American rock band from Chapel Hill, North Carolina.\n\nPassages:\n\n[The Black Keys]\nThe Black Keys are an American rock band formed in Akron, Ohio, in 2001.\n\n[Polvo]\nPolvo is an American indie noise rock band from Chapel Hill, North Carolina.\n\n[Shapes (album)]\nShapes is Polvo's fourth studio album.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb9cd1715a8",
  "kind": "yes/no",
  "text": "Claim: The producer of Back to the World (Street Dogs album), is the Executive Vice President of A&R at this company, while Rod Stewart isn't. The company signed Brian Wilson in 1962.\n\nPassages:\n\n[Nate Albert]\nNate Albert (born 1970) is an American music executive, songwriter, producer and guitar player. He is currently the Executive Vice President of A&R at Capitol Records a division of Universal Music Group.\n\n[Back to the World (Street Dogs album)]\nThe album was produced by Nate Albert, formerly of The Mighty Mighty Bosstones.\n\n[Brian Wilson]\nAfter signing with Capitol Records in 1962, Wilson wrote or co-wrote more than two dozen Top 40 hits for the group.\n\n[Rod Stewart]\nSir Roderick David \"Rod\" Stewart, {'1': \", '2': \", '3': \", '4': \"} (born 10 January 1945) is a British rock singer and songwriter.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc0b28c23eb",
  "kind": "yes/no",
  "text": "Claim: The institution that The New Freedmen's Clinic is affiliated with and another medical center are both located in Washington, D.C. Michael Zasloff worked as a Scientific Director at the other medical center in Virginia.\n\nPassages:\n\n[Howard University Hospital]\nHoward University Hospital, previously known as Freedmen's Hospital, is a major hospital lcated in Washington, D.C., built on the site of the previous Griffith Stadium.\n\n[MedStar Georgetown University Hospital]\nIt is a not-for-profit, acute care teaching and research facility located in the Georgetown neighborhood of the Northwest Quadrant of Washington, D.C.\n\n[The New Freedmen's Clinic]\nThe New Freedmen's Clinic (first opened in the summer of 2009) is a free student-run health care clinic affiliated with Howard University Hospital (HUH) and Howard University College of Medicine (HUCM).\n\n[Michael Zasloff]\nHe is currently Scientific Director, MedStar-Georgetown Transplant Institute, Georgetown University Hospital.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q631c901bc7",
  "kind": "yes/no",
  "text": "Claim: The nationality of the costume designer of Homage to the Queen was English.\n\nPassages:\n\n[Homage to the Queen]\nHomage to the Queen, Op. 42, by Malcolm Arnold was written as the official coronation ballet in 1953, commissioned by the Sadler's Wells Ballet in honour of Queen Elizabeth II, the ballet company's musical adviser Humphrey Searle having recommended Arnold for the job. It was first performed by the Sadler's Wells Ballet on Coronation night 2 June 1953 at the Royal Opera House Covent Garden, with original scenery and costumes by Oliver Messel.\n\n[Oliver Messel]\nOliver Hilary Sambourne Messel (13 January 1904 – 13 July 1978) was an English artist and one of the foremost stage designers of the 20th century.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qf20f671bed",
  "kind": "yes/no",
  "text": "Claim: Thon Marial Maker, a Sudanese-born Australian professional basketball player for the Milwaukee Bucks exemplifies that players do not have to play at least a year in college basketball before being drafted into the NBA.\n\nPassages:\n\n[Thon Maker]\nThon Marial Maker (born 25 February 1997) is a Sudanese-born Australian professional basketball player for the Milwaukee Bucks of the National Basketball Association (NBA).\n\n[NBA high school draftees]\nThe NBA high school draftees are players who have been drafted to the National Basketball Association (NBA) straight out of high school without playing basketball at the collegiate level. Contrary to popular belief, the player does not have to play at least a year in college basketball, as the player can choose to instead play in another professional league (especially overseas) like Brandon Jennings or Emmanuel Mudiay in Italy and China respectively, simply take the year off, such as the case with Satnam Singh Bhamara, or even hold themselves back a year in high school before declaring for the draft, such as the case with Thon Maker.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe89577151d",
  "kind": "yes/no",
  "text": "Tweet: alllllll nighter. woohoo",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q9b6653d8fb",
  "kind": "yes/no",
  "text": "Claim: Rooster is the colloquial name of the professional football team in which this striker, who scored in Syria's 3-0 victory over Spain in the 2013 FIFA Confederations Cup Final, played.\n\nPassages:\n\n[Clube Atlético Mineiro]\nClube Atlético Mineiro (] ), commonly known as Atlético Mineiro or Atlético, and colloquially as Galo (] , \"Rooster\"), is a professional football club based in Belo Horizonte, Minas Gerais, Brazil.\n\n[2013 FIFA Confederations Cup Final]\nBrazil defeated Spain 3–0 with goals from Fred and Neymar, thus breaking Spain's record of 29 games without a defeat.\n\n[Fred (footballer)]\nFrederico Chaves Guedes (born 3 October 1983), known as Fred (] ), is a Brazilian professional footballer who plays as a striker for Campeonato Brasileiro Série A club Atlético Mineiro.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q7f36b311ee",
  "kind": "yes/no",
  "text": "Claim: Fairview is the birthplace of the 23rd United States Secretary of War born in 1874.\n\nPassages:\n\n[Fairview, Kentucky]\nFairview is a small census-designated place on the boundary between Christian and Todd counties in the western part of the U.S. state of Kentucky. It is chiefly notable as the birthplace of Jefferson Davis, later President of the Confederate States of America, and as the location of the Jefferson Davis State Historic Site.\n\n[Jefferson Davis]\nHe was the 23rd United States Secretary of War, serving under U.S. President Franklin Pierce from 1853 to 1857.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qeb8a21f8dc",
  "kind": "yes/no",
  "text": "Claim: The netflix series, produced by Dia, that had an actress best known for her role as Vanessa on \"Atlanta\" also starred Evan Jonigkeit.\n\nPassages:\n\n[Zazie Beetz]\nZazie Beetz (born 1991) is a German-born, American actress best known for the role of Vanessa on \"Atlanta\".\n\n[Evan Jonigkeit]\nEvan Jonigkeit (pronounced \"John-a-kite\",born August 25, 1983) is an American actor known for his roles in \"\", \"Bone Tomahawk\", and \"Easy\".\n\n[Easy (TV series)]\nEasy is a comedy-drama anthology series written, directed, edited and produced by Joe Swanberg.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q793b048f1f",
  "kind": "yes/no",
  "text": "Tweet: Love everything in my basket selling our before the sale was meant to start😒 @ZARA_Care @zara",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qf746747d5a",
  "kind": "yes/no",
  "text": "Claim: A sports group lost in the quarterfinals of the NCAA Tournament. They lost to the team that represented Santa Clara University that was founded in 1851. The losing sports group were defeated by San Diego State in the 2016 Diamond Head Classic.\n\nPassages:\n\n[2016 Diamond Head Classic]\nSan Diego State defeated San Francisco to win the tournament championship.\n\n[2016–17 San Francisco Dons men's basketball team]\nThey lost in the quarterfinals of the WCC Tournament to Santa Clara.\n\n[2016–17 Santa Clara Broncos men's basketball team]\nThe 2016–17 Santa Clara Broncos men's basketball team represented Santa Clara University during the 2016–17 NCAA Division I men's basketball season.\n\n[Santa Clara University]\nFounded in 1851, Santa Clara University is the oldest operating institution of higher learning in California, and has remained in its original location for 166 years.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q87f0679978",
  "kind": "yes/no",
  "text": "Claim: The 2015 San Diego Padres season had former Texas Rangers assistant GM A. J. Preller as a general manager.\n\nPassages:\n\n[A. J. Preller]\nA. J. Preller is the general manager of the San Diego Padres Major League Baseball club. He was hired by the Padres on August 5, 2014 while serving as the assistant GM for the Texas Rangers.\n\n[2015 San Diego Padres season]\nGeneral Manager A. J. Preller had a busy offseason, acquiring a new starting outfield in Matt Kemp, Justin Upton, and Wil Myers, while adding to an already strong bullpen with All-Star closer Craig Kimbrel.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc3167bdfa6",
  "kind": "yes/no",
  "text": "Claim: The proper name of the husband of Lollia Paullina was Gaius Julius Caesar Augustus Germanicus.\n\nPassages:\n\n[Lollia Paulina]\nLollia Paulina, also known as Lollia Paullina (15-49) was a Roman Empress for six months in 38 as the third wife and consort of the Roman emperor Caligula.\n\n[Caligula]\nCaligula ( ), properly Gaius Julius Caesar Augustus Germanicus (31 August AD 12 – 24 January AD 41) was Roman emperor from AD 37–41.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qd2ce75ed6c",
  "kind": "yes/no",
  "text": "Claim: The host of the show that featured clips by Naathan Phan appears in stand-up comedy tours.\n\nPassages:\n\n[Naathan Phan]\nNaathan Phan (commonly known by his screen name, \"SungHero\") (born August 20, 1988) is an Asian Scottish magician, actor, and internet personality whose clips have been featured on Tosh.0.\n\n[Tosh.0]\nTosh.0 ( ) is an American television series hosted and produced by comedian Daniel Tosh, who provides commentary on online viral video clips, society, celebrities, and other parts of popular culture and stereotypes.\n\n[Daniel Tosh]\nHe is known for his deliberately offensive and controversial style of black comedy, as the host of the Comedy Central television show \"Tosh.0\" and as the star of stand-up comedy tours and specials.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb46cb77392",
  "kind": "yes/no",
  "text": "Claim: Crosstown Plaza in Schenectady, NY is near a major interstate. Route 146, this interstate and the I-90 are Highways that run North and South through Schenectady, New York.\n\nPassages:\n\n[Fort Hunter, Albany County, New York]\nFort Hunter lies along New York Route 146 near the Albany-Schenectady county line.\n\n[Crosstown Plaza (Schenectady, NY)]\nCrosstown Plaza is a large strip mall in Schenectady, NY (at the Rotterdam-Schenectady line) along Watt Street and NY State Route 7 near the I-890 entrance.\n\n[Interstate 890]\nInterstate 890 (I-890) is a 9.45 mi long auxiliary Interstate Highway in the vicinity of Schenectady, New York, in the United States. The highway runs southeast–northwest from an interchange with the New York State Thruway (I-90) northwest of Schenectady to another junction with the Thruway south of the city and passes through Downtown Schenectady along the way.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q7d3179cb4d",
  "kind": "yes/no",
  "text": "Claim: An airport is located one nautical mile (2 km) south of the central business district of a town with a population of 583. The attraction, World's Largest Farm Tractor, in 1998, could be found in this town.\n\nPassages:\n\n[Big Bud 747]\nIt is billed by the owners and exhibitors as the \"World's Largest Farm Tractor\".\n\n[Big Sandy Airport]\nIt is owned by the Town of Big Sandy and located one nautical mile (2 km) south of its central business district.\n\n[Big Sandy, Montana]\nThe population was 598 at the 2010 census. Big Sandy, Montana, is where the Big Bud 747, the largest farm tractor in the world, was located from 1997 until 2009.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qf2665193e1",
  "kind": "yes/no",
  "text": "Claim: The metafamily of graphical operating systems developed, marketed, and sold by Microsoft offers software for operatic singing training.\n\nPassages:\n\n[Microsoft Windows]\nMicrosoft Windows, or simply Windows, is a metafamily of graphical operating systems developed, marketed, and sold by Microsoft.\n\n[Winsingad]\nWinSingad is a Microsoft Windows based software for singing training.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q2fd2cc648a",
  "kind": "yes/no",
  "text": "Tweet: oh you’re just friends?\n\nwhy’d u shave then?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 }
]
