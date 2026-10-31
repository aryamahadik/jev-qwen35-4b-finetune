# A46 replay label-noise blind read RSBS06-blind_read-617b2352-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS06-blind_read-617b2352-000.json

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
  "qid": "qd1733a9f2f",
  "kind": "yes/no",
  "text": "Claim: Ernst Messerschmid and Reinhold Ewald ESA were not both astronauts.\n\nPassages:\n\n[Ernst Messerschmid]\nProf. Dr. Ernst Willi Messerschmid (born May 21, 1945) is a German physicist and former astronaut.\n\n[Reinhold Ewald]\nDr. Reinhold Ewald (born December 18, 1956) is a German physicist and ESA astronaut.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q5294df8b60",
  "kind": "yes/no",
  "text": "Claim: Sterling Jewelers was bought by another company in 1987. The company also owns Zale Corporation, a Delaware based retailer, along with H. Samuel and Jared.\n\nPassages:\n\n[Signet Jewelers]\nSignet Jewelers owns and operates the companies Zales, Kay Jewelers, and Jared.\n\n[Sterling Jewelers]\nSterling Jewelers is a wholly owned subsidiary of UK-based Signet Jewelers Limited (listed on the New York Stock Exchange under the symbol SIG), having been acquired in 1987.\n\n[Zale Corporation]\nThe Zale Corporation is an American jewelry retailer, incorporated in Delaware in 1993.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q5e3525db8b",
  "kind": "yes/no",
  "text": "Claim: The band that collaborated with Neva Dinova on the album \"One Jug of Wine, Two Vessels\" is a rock band from America. As is the band that were on the album Dracula 2000 (soundtrack).\n\nPassages:\n\n[Dracula 2000 (soundtrack)]\nThe soundtrack contains music from heavy rock/metal artists, including Pantera, Disturbed, Powerman 5000, Godhead with Marilyn Manson, System of a Down, Linkin Park, Taproot, Hed Planet Earth, Saliva, and many more.\n\n[Bright Eyes (band)]\nBright Eyes is an American indie rock band founded by singer-songwriter and guitarist Conor Oberst.\n\n[Disturbed (band)]\nDisturbed is an heavy metal band from Homer Glen, Illinois, formed in 1996.\n\n[One Jug of Wine, Two Vessels]\nOne Jug of Wine, Two Vessels is a collaborative split EP by Bright Eyes and Neva Dinova.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q28744d4541",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "\"I really don't like that I am still getting as frustrated over websites crashing when I'm buying tickets as I did when I was younger\"",
   "i’m sure 14 year old me would be delighted to know that 22 year old me is still getting stressed over websites crashing for bands🙃"
  ]
 },
 {
  "qid": "qd025022728",
  "kind": "yes/no",
  "text": "Claim: In 2005 the manager of the singer-songwriter best known for \"American Pie\" died.\n\nPassages:\n\n[Harold Leventhal]\nHarold Leventhal (May 24, 1919 – October 4, 2005) was an American music manager. He died in 2005 at the age of 86. He managed The Weavers, Woody Guthrie, Pete Seeger, Alan Arkin, Judy Collins, Theodore Bikel, Arlo Guthrie, Joan Baez, Mary Travers, Tom Paxton, Don McLean and many others.\n\n[Don McLean]\nDonald McLean III (born October 2, 1945) is an American singer-songwriter best known for \"American Pie\", an RIAA \"Song of the Century\" (position 5 of 25), about the changes in American society from the late 1950s to the early 1970s, through metaphorical references to the music industry during those years.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q967daf3690",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "\"Ah yes, another afternoon with the WiFi down...makes working from home completely unbearable\"",
   "Ah yes, another afternoon with the WiFi down...really makes working from home that extra bit more enjoyable :)"
  ]
 },
 {
  "qid": "q7a2c02b548",
  "kind": "yes/no",
  "text": "Claim: Pasquale Pistoriois the ex-president of a multinational electronics and semiconductor manufacturer headquartered in northern Geneva.\n\nPassages:\n\n[STMicroelectronics]\nSTMicroelectronics is a French-Italian multinational electronics and semiconductor manufacturer headquartered in Geneva, Switzerland.\n\n[Pasquale Pistorio]\nPasquale Pistorio (Agira, 6 January 1936) is an Italian company director, ex president of STMicroelectronics and board member of Confindustria.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q5f6f0fe1e7",
  "kind": "yes/no",
  "text": "Claim: A star of The Great White Hype played General Pushkin in a Bond Film. That film starred Timothy Dalton as the politician in which the fictional organization SPECTRE is featured in.\n\nPassages:\n\n[John Rhys-Davies]\nHe also played Agent Michael Malone in the 1993 remake of the 1950s television series \"The Untouchables\", Pilot Vasco Rodrigues in the mini-series \"Shōgun\", Professor Maximillian Arturo in \"Sliders\", King Richard I in \"Robin of Sherwood\", General Leonid Pushkin in the James Bond film \"The Living Daylights\", and Macro in \"I, Claudius\".\n\n[SPECTRE]\nSPECTRE (SPecial Executive for Counterintelligence, Terrorism, Revenge and Extortion) is a fictional organisation featured in the James Bond novels by Ian Fleming, the films based on those novels, and James Bond video games.\n\n[The Great White Hype]\nIt stars Samuel L. Jackson, Peter Berg, Damon Wayans, Jeff Goldblum, Jon Lovitz, Cheech Marin, John Rhys-Davies, Salli Richardson and Jamie Foxx.\n\n[The Living Daylights]\nThe Living Daylights (1987) is the fifteenth entry in the \"James Bond\" film series and the first to star Timothy Dalton as the fictional MI6 agent James Bond.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q03486f1949",
  "kind": "yes/no",
  "text": "Claim: Harry Beaumont and Theodore Wharton were not co-owners in a movie.\n\nPassages:\n\n[Harry Beaumont]\nHarry Beaumont (February 10, 1888 – December 22, 1966) was an American film director, actor, and screenwriter. He worked for a variety of production companies including Fox, Goldwyn, Metro, Warner Brothers, and Metro-Goldwyn-Mayer.\n\n[Theodore Wharton]\nTheodore Wharton (1875–1931) was an American film director, producer and writer.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe80fd0ca9a",
  "kind": "yes/no",
  "text": "Claim: The mainly Jewish Tangier town in Virginia speaks the High Tider dialect and has lost 67% of its landmass since 1850.\n\nPassages:\n\n[High Tider]\nHigh Tider or \"Hoi Toider\" is a dialect of American English spoken in very limited communities of the South Atlantic United States—particularly, several small island and coastal townships of the rural North Carolina \"Down East\" seaside region that encompasses the Outer Banks and Pamlico Sound (specifically including Atlantic, Sea Level, and Harkers Island in eastern Carteret County, and also Ocracoke) as well as of the Chesapeake Bay (such as Tangier and Smith Island).\n\n[Tangier, Virginia]\nSince 1850, the island's landmass has been reduced by 67%.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qcc5562160c",
  "kind": "yes/no",
  "text": "Claim: The Rainmaker starred the actor who has been nominated for two British Academy Film Awards.\n\nPassages:\n\n[The Rainmaker (1997 film)]\nIt stars Matt Damon, Danny DeVito, Danny Glover, Claire Danes, Jon Voight, Roy Scheider, Mickey Rourke, Virginia Madsen, Mary Kay Place and Teresa Wright in her final film role.\n\n[Matt Damon]\nDamon has received various accolades, including an Academy Award from five nominations, two Golden Globe Awards from eight nominations, and has been nominated for two British Academy Film Awards and six Emmy Awards.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q775430cf12",
  "kind": "yes/no",
  "text": "Claim: Terrace on the Park is a banquet hall located in this amenity. The borough where this amenity is situated had a 20% bigger population than Staten Island in the 2016 census.\n\nPassages:\n\n[Queens]\nCoterminous with Queens County since 1899, the borough of Queens is the second-largest in population (after Brooklyn), with a census-estimated 2,333,054 residents in 2016, approximately 48% of them foreign-born.\n\n[Staten Island]\nWith a 2016 Census-estimated population of 476,015, Staten Island is the least populated of the boroughs but is the third-largest in area at 58 sqmi .\n\n[Flushing Meadows–Corona Park]\nLocated in the borough of Queens, it is between I-678 (Van Wyck Expressway) and the Grand Central Parkway and stretches from Flushing Bay, at the southern edge of LaGuardia Airport, to Union Turnpike.\n\n[Terrace on the Park]\nTerrace on the Park is a banquet hall in Flushing Meadows–Corona Park.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q381ede5dc5",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which text is sarcastic?",
  "options": [
   "I hate working outside in the heat.",
   "I just absolutely LOVE how I've got to work outside for the next 3 days in the heatwave. #sweatingmyballsoff"
  ]
 },
 {
  "qid": "qf97afa97f5",
  "kind": "yes/no",
  "text": "Claim: Mawson is an electoral district that includes the wine regional around the town, where Mollydooker Wines Pty Ltd, originated in 1925 is based, 35 km south of Adelaide.\n\nPassages:\n\n[Mollydooker Wines]\nMollydooker Wines Pty Ltd is based in the McLaren Vale Area of Australia.\n\n[McLaren Vale]\nMcLaren Vale is a wine region approximately 35 km south of Adelaide in South Australia.\n\n[Electoral district of Mawson]\nMawson is an electoral district of the House of Assembly in the Australian state of South Australia. It covers most of the outer southern suburbs of the City of Onkaparinga, including Hackham, Hackham West, Huntfield Heights, Noarlunga Downs, Old Noarlunga, Onkaparinga Hills and Seaford Heights, the regional shopping centre area at Noarlunga Centre, parts of Woodcroft, and the southern wine region around McLaren Vale and Willunga.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qeca76ef58b",
  "kind": "yes/no",
  "text": "Claim: Carlos Ashley Raphael \"Carl\" Barât has been in more bands in his life than another singer/songwriter. This singer/songwriter fronted a punk band who released Expansive Heart.\n\nPassages:\n\n[Carl Barât]\nCarlos Ashley Raphael Barât (born 6 June 1978) is a British musician, best known for being the co-frontman with Peter Doherty of the garage rock band The Libertines. He was the frontman and lead guitarist of Dirty Pretty Things, and in 2010 debuted a solo album. In 2014 he announced the creation of his new band, The Jackals.\n\n[Expansive Heart]\nExpansive Heart is the only piece ever released by punk band Big Rig, it was released on the Lookout!\n\n[Big Rig (band)]\nBig Rig was a punk band from the San Francisco Bay Area fronted by singer/songwriter Jesse Michaels.\n\n[Jesse Michaels]\nJesse Michaels is a songwriter, vocalist, guitarist and artist from Berkeley, California. He is most well known as the vocalist for the ska punk band Operation Ivy.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qeb7dfac9fd",
  "kind": "yes/no",
  "text": "Claim: The creator of \"Too Romantic\" was born before Aaron Katz.\n\nPassages:\n\n[Aaron Katz (filmmaker)]\nAaron Katz (born October 29, 1981) is an award-winning independent American filmmaker from Portland, Oregon.\n\n[Too Romantic]\nToo Romantic is a 1992 dramatic short film that Todd Field created while a fellow at the AFI Conservatory.\n\n[Todd Field]\nWilliam Todd Field (born February 24, 1964) is an American actor and three-time Academy Award nominated filmmaker.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q49096c6d0d",
  "kind": "yes/no",
  "text": "Claim: West of Broadway is a lost 1926 American silent romantic comedy/Western film. Its director was born before the director of \"Simon Birch\".\n\nPassages:\n\n[Simon Birch]\nSimon Birch is a 1998 American comedy-drama film loosely based on \"A Prayer for Owen Meany\" by John Irving and was directed and written for the screen by Mark Steven Johnson.\n\n[Robert Thornby]\nRobert Thornby (March 27, 1888 – March 6, 1953) was an American director and actor of the silent era.\n\n[West of Broadway]\nWest of Broadway is a lost 1926 American silent romantic comedy/Western film directed by Robert Thornby and starring Priscilla Dean.\n\n[Mark Steven Johnson]\nMark Steven Johnson (born October 30, 1964) is an American screenwriter, film director, and producer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q86d3b6ef1f",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Overthinking everything in life really takes a toll on you",
   "There is a contrast between the word \"overthinking\" and how everything in life really does not take a toll on you."
  ]
 },
 {
  "qid": "q0bafe61475",
  "kind": "yes/no",
  "text": "Claim: Anna B. Sheppard has worked in films with Steven Allan Spielberg, a part of the New Hollywood era.\n\nPassages:\n\n[Anna B. Sheppard]\nA sister to fellow costume designer Magdalena Biedrzycka, Sheppard made many films with directing masters like Steven Spielberg or Roman Polański.\n\n[Steven Spielberg]\nSteven Allan Spielberg, {'1': \", '2': \", '3': 'KBE', '4': \"} , {'1': \", '2': \", '3': 'OMRI', '4': \"} (born December 18, 1946) is an American director, producer, and screenwriter. He is considered one of the founding pioneers of the New Hollywood era, as well as being viewed as one of the most popular directors and producers in film history.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qdc35e9c4c0",
  "kind": "yes/no",
  "text": "Claim: National Contest Journal is published with an independent volunteer editor, not Doctor Who Magazine.\n\nPassages:\n\n[National Contest Journal]\nThe National Contest Journal (also referred to by the acronym NCJ) is a bimonthly magazine published by the American Radio Relay League, with an independent volunteer editor.\n\n[Doctor Who Magazine]\nIts current editor is Marcus Hearn, who took over from the magazine's longest-serving editor, Tom Spilsbury, in July 2017.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q68d897bea0",
  "kind": "yes/no",
  "text": "Claim: The musician from another band who released a famous album joined the group Zwan shortly after its breakup. FOL (song) appeared on on this album.\n\nPassages:\n\n[Zeitgeist (The Smashing Pumpkins album)]\nZeitgeist is the seventh album by American alternative rock band The Smashing Pumpkins, released on July 10, 2007 in the United States and Canada. The album was produced by Roy Thomas Baker, Billy Corgan, Jimmy Chamberlin, and Terry Date.\n\n[Jimmy Chamberlin]\nHe is best known as the drummer for the alternative rock band The Smashing Pumpkins. Following the 2000 breakup of the band, Chamberlin joined Pumpkins frontman Billy Corgan in the supergroup Zwan and also formed his own group, the Jimmy Chamberlin Complex.\n\n[FOL (song)]\n\"FOL\" is a song by The Smashing Pumpkins, written and recorded during the sessions for their 2007 album \"Zeitgeist\" and used for a Hyundai commercial during Super Bowl XLIII.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qf09f604817",
  "kind": "yes/no",
  "text": "Claim: The band who recorded the album Barely Legal is from Sweden. Broder Daniel is from that same country.\n\nPassages:\n\n[Broder Daniel]\nBroder Daniel (Swedish: \"Brother Daniel\"), often abbreviated as BD, was an alternative rock band from Gothenburg, Sweden.\n\n[The Hives]\nThe Hives are a Swedish rock band that rose to prominence in the early 2000s during the garage rock revival.\n\n[Barely Legal (album)]\nBarely Legal is the debut studio album by Swedish rock band The Hives, from Fagersta, Sweden.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q0fb027da4b",
  "kind": "yes/no",
  "text": "Claim: Robert Earl Holding owned an oil company that was originally founded by Harry F. Sinclair.\n\nPassages:\n\n[Robert Holding]\nRobert Earl Holding (November 29, 1926 – April 19, 2013) was an American businessman who owned Sinclair Oil Corporation, the Little America Hotels, the Grand America Hotel, the Westgate Hotel in San Diego, California (directed by Georg Hochfilzer), and two ski resorts, Sun Valley in central Idaho since 1977, and Snowbasin near Ogden, Utah, since 1984.\n\n[Sinclair Oil Corporation]\nSinclair Oil Corporation is an American petroleum corporation, founded by Harry F. Sinclair on May 1, 1916, as the Sinclair Oil and Refining Corporation by combining the assets of 11 small petroleum companies.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qb8b5e323a9",
  "kind": "yes/no",
  "text": "Tweet: Just because its 27 degrees outside doesn't mean I won't pretend its 7 degrees so I can wrap up in blankets, drink autumn coffee, put candles on and think about all things spooky",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q5ec7460dec",
  "kind": "yes/no",
  "text": "Claim: The writers Bobbie Ann Mason and the author of \"Elizabeth Appleton\" share the same Belgium nationality.\n\nPassages:\n\n[Elizabeth Appleton]\nElizabeth Appleton is a novel by John O'Hara first published in 1963.\n\n[Bobbie Ann Mason]\nBobbie Ann Mason (born May 1, 1940) is a Southern United States novelist, short story writer, essayist, and literary critic from Kentucky.\n\n[John O'Hara]\nJohn Henry O'Hara (January 31, 1905 – April 11, 1970) was an American writer, best remembered as a keen observer of social status and manners in early to mid 20th century America and pre-eminent among his contemporaries at depicting social realism.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q6dfbc1b911",
  "kind": "yes/no",
  "text": "Claim: In between the husband of Nora Balling and Micky Dolenz, George Michael Dolenz was the a member of the Monkees.\n\nPassages:\n\n[Nora Balling]\nNora-Isabelle Balling, also known as Nora Anders (born July 31, 1964, Koblenz, Germany) is a German fashion model, and was the first wife of the singer and former Modern Talking member, Thomas Anders, between 1984 and 1999.\n\n[Thomas Anders]\nThomas Anders (born Bernd Weidung, 1 March 1963) is a German singer, composer, and record producer.\n\n[Micky Dolenz]\nGeorge Michael Dolenz, Jr. (born March 8, 1945) is an American actor, musician, television director, radio personality and theater director, best known as a vocalist and drummer of the 1960s pop/rock band the Monkees.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q31edc4ab7d",
  "kind": "yes/no",
  "text": "Claim: The director of \"Dedication of the Great Buddha\" was older than master chef Don O. Newland when he died.\n\nPassages:\n\n[Teinosuke Kinugasa]\nTeinosuke Kinugasa (衣笠 貞之助 , Kinugasa Teinosuke ) (1 January 1896 – 26 February 1982) was a Japanese actor and film director.\n\n[Dedication of the Great Buddha]\nDedication of the Great Buddha (大仏開眼 , Daibutsu kaigen ) is a 1952 Japanese film directed by Teinosuke Kinugasa.\n\n[Don O. Newland]\nDon Oliver Newland (1896–1951) was an American film director and producer whose career consisted largely of itinerant work.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q0bacd800c0",
  "kind": "yes/no",
  "text": "Claim: Louis XIV was formed after the band whose first full album was Up from Below.\n\nPassages:\n\n[Edward Sharpe and the Magnetic Zeros]\nEdward Sharpe and the Magnetic Zeros is an American folk rock band formed in Los Angeles, California in 2007.\n\n[Up from Below]\nUp from Below is the first full-length album from Edward Sharpe and the Magnetic Zeros.\n\n[Louis XIV (band)]\nLouis XIV is an American rock band from San Diego, California. The band has released four EPs between 2003 and 2007, and three albums between 2003 and 2008, the latter two of which were distributed by Atlantic Records.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q5fd832f2d7",
  "kind": "yes/no",
  "text": "Post: Thank you to my apartment complex for consistently cutting the grass at 8 am every Thursday for ~5 hours. It’s definitely not super obnoxious or bothersome ☺️☺️",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q1cf849786d",
  "kind": "yes/no",
  "text": "Claim: Kamal Haasan starred in a film directed by the director of \"Sundara Swapnagalu\".\n\nPassages:\n\n[Sundara Swapnagalu]\nThe film was a remake of director's own Tamil film \"Sollathaan Ninaikkiren\".\n\n[Sollathaan Ninaikkiren]\nSollathaan Ninaikkiren is a 1973 Tamil language film scripted and directed by K. Balachander starring Sivakumar, S. V. Subbaiah, Jayachitra, Srividya, Shubha, Kamal Haasan and Jayasudha in the lead roles.\n\n[Kamal Haasan]\nKamal Haasan (born 7 November 1954) is an Indian film actor, director, screenwriter, producer, playback singer and lyricist who works primarily in Tamil cinema.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q8bbbfbf7c0",
  "kind": "yes/no",
  "text": "Post: it's all about women in stem struggles. what about women in interactive media struggles: i no longer win against my friends in smash because they major in goddamn video game.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q70e77a0563",
  "kind": "yes/no",
  "text": "Claim: Theories of rhetoric and composition pedagogy, the field of rhetoric has been a matter of considerable debate for millennia, Aristotle, was an ancient Greek philosopher, theorist and scientist born in the city of Stagira, Chalkidice, on the northern periphery of Classical Greece.\n\nPassages:\n\n[Theories of rhetoric and composition pedagogy]\nAristotle wrote a philosophical work that still has major scholarly impact, \"Rhetoric\", in which he identifies five canons of the field of rhetoric: invention, arrangement, style, memory, and delivery.\n\n[Aristotle]\nAristotle ( ; Greek: Ἀριστοτέλης , , \"Aristotélēs\"; 384–322 BC) was an ancient Greek philosopher and scientist born in the city of Stagira, Chalkidice, on the northern periphery of Classical Greece.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q9cbd58e37b",
  "kind": "yes/no",
  "text": "Text: quackity stream is making me so genuinely happy rn",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q75bcb7bad1",
  "kind": "yes/no",
  "text": "Tweet: it'd be nice if missguided actually had stock for once🙂🙂🙂",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q2d821e4664",
  "kind": "yes/no",
  "text": "Claim: Farallon Capital was founded by a hedge fund manager born in the year 1957.\n\nPassages:\n\n[Farallon Capital]\nThe firm was founded by Tom Steyer in 1986.\n\n[Tom Steyer]\nThomas Fahr Steyer (born June 27, 1957) is an American hedge fund manager, philanthropist, environmentalist, liberal activist, and fundraiser.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q8601c2f0ba",
  "kind": "yes/no",
  "text": "Claim: August 27, 1952 is the birth date of the former Trump campaign manager who promoted Jack Posobiec's tweets.\n\nPassages:\n\n[Roger Stone]\nRoger Jason Stone Jr. (born August 27, 1952) is an American political consultant, lobbyist, and strategist, noted for his use of opposition research usually for candidates of the Republican Party.\n\n[Jack Posobiec]\nHe was granted press access to the White House in April 2017, and his tweets have been promoted by former Trump campaign manager Roger Stone.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qea574e5129",
  "kind": "yes/no",
  "text": "Claim: The United States Senate election in Hawaii that took place in 1992 ended with the winning of Japanese-American politician Daniel Ken \"Dan\" Inouye.\n\nPassages:\n\n[United States Senate election in Hawaii, 1992]\nIncumbent Democrat U.S. Senator Daniel Inouye won re-election to a sixth term.\n\n[Daniel Inouye]\nDaniel Ken \"Dan\" Inouye (Japanese: 井上 建 , Hepburn: Inoue Ken ) was a United States Senator from Hawaii from 1963 to 2012. He was a member of the Democratic Party, and he was President pro tempore of the United States Senate (third in line in the Presidential Line of Succession) from 2010 until his death in 2012, making him the highest-ranking Japanese American politician in U.S. history.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q3db14ce6e8",
  "kind": "yes/no",
  "text": "Claim: The plaintiff in the 1892 Barbed Wire Patent Case was born on January 18, 1813.\n\nPassages:\n\n[Joseph Glidden]\nJoseph Glidden (January 18, 1813 – October 9, 1906) was an American businessman.\n\n[The Barbed Wire Patent]\nThe Barbed Wire Patent Case, 143 U.S. 275 was a significant patent dispute in 1892 between plaintiff Joseph Glidden and the USPTO regarding the right of barbed wire.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q41bc0d6d45",
  "kind": "yes/no",
  "text": "Claim: Russian-born Victor Oladipo and NBA All-Rookie Team are connected by basketball.\n\nPassages:\n\n[NBA All-Rookie Team]\nThe NBA All-Rookie Team is an annual National Basketball Association (NBA) honor given since the 1962–63 NBA season to the top rookies during the regular season.\n\n[Victor Oladipo]\nKehinde Babatunde Victor Oladipo (born May 4, 1992) is an American professional basketball player for the Indiana Pacers of the National Basketball Association (NBA).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5100381f17",
  "kind": "yes/no",
  "text": "Claim: Wellingrove, New South Wales is 20 miles northwest of the parish and town in New England NSW.\n\nPassages:\n\n[Glen Innes, New South Wales]\nGlen Innes is a parish and town on the Northern Tablelands, in the New England region of New South Wales, Australia.\n\n[Wellingrove, New South Wales]\nWellingrove is a village located on the Wellingrove Road about 20 kilometres north west of Glen Innes, New South Wales on the Northern Tablelands, New South Wales, Australia.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q743bb2758f",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "My nose is awful",
   "if 2020 was a nose it’d be mine 🐦"
  ]
 },
 {
  "qid": "qbb83c08161",
  "kind": "yes/no",
  "text": "Claim: The star of the 1987 film Loha's maternal grandfather delivered Shakespeare performances.\n\nPassages:\n\n[Karan Kapoor]\nHis maternal grandparents, Geoffrey Kendal and Laura Kendal, were actors who toured India and Asia with their theatre group, Shakespeareana, performing Shakespeare and Shaw.\n\n[Loha (1987 film)]\nIt stars Dharmendra, Shatrughan Sinha, Karan Kapoor, Madhavi, Mandakini and Amrish Puri.\n\n[Geoffrey Kendal]\nGeoffrey Kendal (7 September 1909 – 14 May 1998) was an English actor-manager who delivered Shakespeare performances throughout India in the 1940s and 1950s.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qeeb7d384c2",
  "kind": "yes/no",
  "text": "Claim: The author of The Lost World (Crichton novel) is not an actor. McG is also not an actor.\n\nPassages:\n\n[The Lost World (Crichton novel)]\nThe Lost World is a techno thriller novel written by Michael Crichton and published in 1995 by Knopf.\n\n[McG]\nJoseph McGinty Nichol (born August 9, 1968), known mononymously as McG, is an American director, producer, and former record producer.\n\n[Michael Crichton]\nJohn Michael Crichton ( ; October 23, 1942 – November 4, 2008) was an American best-selling author, screenwriter, film director and producer best known for his work in the science fiction, medical fiction and thriller genres.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q9f27d62e7d",
  "kind": "yes/no",
  "text": "Claim: Best of the 'B' Sides excludes \"I Live My Way\". The A side of this record was included on the soundtrack of a film whose star was born in 1944.\n\nPassages:\n\n[Michael Douglas]\nMichael Kirk Douglas (born September 25, 1944) is an American actor and producer.\n\n[Best of the 'B' Sides]\nIt covers all of their singles from their first (1980's \"Running Free\") to 2000's \"Out of the Silent Planet\", although several of the band's original B-sides were excluded from the collection: \"Total Eclipse\" (from \"Run to the Hills\", 1982, although this has been added to the album \"The Number of the Beast\" from 1998 onwards), \"Mission From 'Arry\" (from \"2 Minutes to Midnight\", 1984); \"Bayswater Ain't a Bad Place to Be\" (from \"Be Quick or Be Dead\", 1992); and \"I Live My Way\" (from \"Man on the Edge\", 1995).\n\n[Man on the Edge]\nThe song is based on the film \"Falling Down\", starring Michael Douglas.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q0d46f6631c",
  "kind": "yes/no",
  "text": "Post: Leave it to the nice people of Hutch to yell at me to \"eat shit\" while I run. Jokes on them, I do.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qc33fa08cc5",
  "kind": "yes/no",
  "text": "Claim: The American actor and singer Brady Bluhm plays a fictional character in a film series based on a character from Return to the Hundred Acre Wood. That fictional character appears in the stories of a fictional anthropomorphic teddy bear.\n\nPassages:\n\n[Winnie-the-Pooh]\nWinnie-the-Pooh, also called Pooh Bear, is a fictional anthropomorphic teddy bear created by English author A. A. Milne.\n\n[Brady Bluhm]\nHe is the brother of actor Brandon Bluhm, and is best known for his role as Christopher Robin in many \"Winnie the Pooh\" films.\n\n[Christopher Robin]\nHe appears in Milne's popular books of poetry and Winnie-the-Pooh stories and is named after Christopher Robin Milne, the author's son.\n\n[Return to the Hundred Acre Wood]\nReturn to the Hundred Acre Wood is a \"Winnie-the-Pooh\" novel published on 5 October 2009.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa4df252f89",
  "kind": "yes/no",
  "text": "Tweet: USA is turning into the 40-something uncle who turns up to the wedding reception, gets drunk &amp; takes the mic from the band to sing Sweet Caroline, but gets all the words wrong.\n\nHighly entertaining but a total fucking train wreck that you’re glad you don’t have to see more often.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q6d3483d473",
  "kind": "yes/no",
  "text": "Claim: This 72-78 passenger aircraft has parking spaces at Nakhon Si Thammarat Airport in Malyasia, which is a Total space of 2,902,400 square meters.\n\nPassages:\n\n[ATR 72]\nThe number \"72\" in its name is derived from the aircraft's standard seating configuration in a passenger-carrying configuration, which could seat 72-78 passengers in a single-class arrangement.\n\n[Nakhon Si Thammarat Airport]\nTotal space, 2,902,400 square meters.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q24803e5314",
  "kind": "yes/no",
  "text": "Claim: The town Caerwys railway station was located in, is situated under four miles from the A55 road also known as the North Wales Expressway.\n\nPassages:\n\n[A55 road]\nThe A55, also known as the North Wales Expressway (Welsh: \"Gwibffordd Gogledd Cymru\") and the Chester to Bangor Trunk Road, is a major road in Britain.\n\n[Afonwen]\nIt is situated just under four miles from the A55 North Wales Expressway and on the A541 Mold-Denbigh road.\n\n[Caerwys railway station]\nCaerwys railway station was a station in Afonwen, Flintshire, Wales.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9594e37083",
  "kind": "yes/no",
  "text": "Claim: In regards to Value premium the expert who argued that no value premium exists, did not found The Vanguard Group.\n\nPassages:\n\n[John C. Bogle]\nHe is the founder and retired chief executive of The Vanguard Group.\n\n[Value premium]\nOther experts, such as John C. Bogle, have argued that no value premium exists, claiming that Fama and French's research is period dependent.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 }
]
