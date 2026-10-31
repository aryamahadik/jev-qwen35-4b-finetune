# A46 replay label-noise blind read RSAS05-blind_read-537c9c01-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS05-blind_read-537c9c01-007.json

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
  "qid": "q449fae18b1",
  "kind": "yes/no",
  "text": "Claim: The LDS Church President that dedicated the This is the Place Monument in Utah, played a more important role in the church than Wong Jing.\n\nPassages:\n\n[Wong Jing]\nWong Jing ( born 3 May 1955) is a Hong Kong film director, producer, actor, presenter, and screenwriter.\n\n[This is the Place Monument]\nIt was dedicated by LDS Church President George Albert Smith on 24 July 1947, the hundredth anniversary of the pioneers entering the Salt Lake Valley.\n\n[George Albert Smith]\nGeorge Albert Smith Sr. (April 4, 1870 – April 4, 1951) was an American religious leader who served as the eighth president of The Church of Jesus Christ of Latter-day Saints (LDS Church).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q394427fdda",
  "kind": "yes/no",
  "text": "Claim: The critically acclaimed author of Bambi's Children: The Story of a Forest Family, originally titled his most famous work Bambi: Eine Lebensgeschichte aus dem Walde.\n\nPassages:\n\n[Bambi's Children]\nBambi's Children: The Story of a Forest Family (German: Bambis Kinder: Eine Familie im Walde ) is a novel written by Austrian author Felix Salten as a sequel to his successful work \"Bambi, A Life in the Woods\".\n\n[Bambi, a Life in the Woods]\nBambi, a Life in the Woods, originally published in Austria as Bambi: Eine Lebensgeschichte aus dem Walde is a 1923 Austrian novel written by Felix Salten and published by Ullstein Verlag.\n\n[Felix Salten]\nFelix Salten (6 September 1869 – 8 October 1945) was an Austrian author and critic in Vienna.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q5830adbce1",
  "kind": "yes/no",
  "text": "Claim: The creator of The Life & Times of Tim and this man are not both art dealers. The other man currently owns the Nathaniel L. McCready House.\n\nPassages:\n\n[Nathaniel L. McCready House]\nIn 2011, the home was purchased by Larry Gagosian, who demolished the mansion's interior.\n\n[The Life &amp; Times of Tim]\nThe series was created by Steve Dildarian, and is about a hapless man in his mid-20s named Tim (voiced by Dildarian) who lives in New York City with his girlfriend Amy.\n\n[Steve Dildarian]\nSteve Dildarian (born November 3, 1969) is an American former advertising copywriter who is the creator, writer, producer and voice of Tim in the HBO animated television series \"The Life & Times of Tim\" (2008-2012).\n\n[Larry Gagosian]\nLawrence Gilbert \"Larry\" Gagosian (born April 19, 1945) is an Armenian American art dealer who owns the Gagosian Gallery chain of art galleries.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qd11164ba5b",
  "kind": "yes/no",
  "text": "Claim: The 1997 independent slapstick comedy film produced by Rudy Rupak, stars this Danish-Italian actress, model, singer and reality television personality who began her career modelling for Greg Gorman and Helmut Newton.\n\nPassages:\n\n[Rudy Rupak]\nHe is also known for producing Snowboard Academy.\n\n[Snowboard Academy]\nSnowboard Academy is a 1997 independent slapstick comedy film, starring Corey Haim, Jim Varney and Brigitte Nielsen.\n\n[Brigitte Nielsen]\nBrigitte Nielsen (born Gitte Nielsen; 15 July 1963) is a Danish-Italian actress, model, singer and reality television personality who began her career modelling for Greg Gorman and Helmut Newton and several years later acted in the 1985 films \"Red Sonja\" and \"Rocky IV\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q778312acd2",
  "kind": "yes/no",
  "text": "Claim: Burnley, a market town in Lancashire, is part of the BB postcode area.\n\nPassages:\n\n[BB postcode area]\nThe BB postcode area, also known as the Blackburn postcode area, is a group of postcode districts around Accrington, Barnoldswick, Blackburn, Burnley, Clitheroe, Colne, Darwen, Nelson and Rossendale in England.\n\n[Burnley]\nBurnley ( ) is a market town in Lancashire, England, with a population of 73,021.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qb56b6b2fdc",
  "kind": "yes/no",
  "text": "Claim: Ohio native William Gladstone Steel helped create Crater Lake National Park, where the lake is most famous for its deep blue color.\n\nPassages:\n\n[William Gladstone Steel]\nWilliam Gladstone Steel (September 7, 1854 – October 21, 1934), called the \"father of Crater Lake\", referring to the creation of Crater Lake National Park in Oregon, United States.\n\n[Crater Lake]\nIt is the main feature of Crater Lake National Park and is famous for its deep blue color and water clarity.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q2e8b764580",
  "kind": "yes/no",
  "text": "Claim: The film that the father of the star of Sultanat starred in in 1970 was Bombay Talkie.\n\nPassages:\n\n[Jennifer Kendal]\nHer other film appearances included \"Bombay Talkie\" (1970), \"Junoon\" (1978), \"Heat and Dust\" (1983), and \"Ghare Baire\" (1984).\n\n[Karan Kapoor]\nHe is the son of Indian Bollywood International Actor Shashi Kapoor and his India settled (late) British Actress Jennifer Kendal.\n\n[Sultanat]\nThe film stars Dharmendra, Sunny Deol, Sridevi, Amrish Puri, Shakti Kapoor, Tom Alter and marked the debut of Karan Kapoor (son of Shashi Kapoor) and Juhi Chawla.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q316ff2bf98",
  "kind": "yes/no",
  "text": "Claim: Trains run on the system which has a terminal station located at the intersection of 32nd Street and Sixth Avenue in the Herald Square neighborhood of Manhattan, New York City 24 hours a day and 7 days a week.\n\nPassages:\n\n[33rd Street station (PATH)]\nLocated at the intersection of 32nd Street and Sixth Avenue in the Herald Square neighborhood of Manhattan, New York City, it is served by the Hoboken–33rd Street and Journal Square–33rd Street lines on weekdays, and by the Journal Square–33rd Street (via Hoboken) line on weekends.\n\n[PATH (rail system)]\nPATH trains run 24 hours a day and 7 days a week.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q2481a16166",
  "kind": "yes/no",
  "text": "Tweet: love it when Jonny makes me use earphones to watch something on my phone so he can play fifa",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q17af9add8b",
  "kind": "yes/no",
  "text": "Post: cant wait to dance with harry styles and the delta variant at their concert in november!!",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q20c89bf121",
  "kind": "yes/no",
  "text": "Claim: The NorthCap University is located in India. The establishment, where the writer of the lyrics for the ASEAN Song of Unity studied for his Ph.D. in Govt, is not.\n\nPassages:\n\n[The Northcap University]\nThe NorthCap University, formerly ITM University, is an autonomous university situated in Sector 23-A, Gurugram, Haryana, India.\n\n[Nicanor Tiongson]\nHe holds a Bachelor of Humanities degree from the Ateneo de Manila University, and M.A. and Ph.D. in Philippine Studies from the University of the Philippines.\n\n[ASEAN Song of Unity]\nThe lyrics were written by Nicanor Tiongson and the music was composed by Ryan Cayabyab.\n\n[University of the Philippines]\nThe University of the Philippines (UP; Filipino: \"Unibersidad ng Pilipinas\" or \"Pamantasan ng Pilipinas\") is a state university system in the Philippines.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qba3b38daa9",
  "kind": "yes/no",
  "text": "Claim: Cathouse: The Series documents the lives of workers in a legal brothel on Moonlight Road. It is a few minutes outside of the birthplace of James Settelmeyer.\n\nPassages:\n\n[James Settelmeyer]\nSettelmeyer was born in Carson City, and now lives and works on his family ranch in Carson Valley.\n\n[Moonlite BunnyRanch]\nThe Moonlite BunnyRanch (often misspelled \"Moonlight\", though that is the correct spelling of the road on which it is addressed) is a legal, licensed brothel in Mound House, Nevada, United States, 6 mi east of Carson City.\n\n[Dennis Hof]\nSeveral of his brothels are in Moundhouse, Nevada, a few minutes outside Carson City.\n\n[Cathouse: The Series]\nCathouse: The Series is an HBO television series that documents the professional lives of the workers at the Moonlite BunnyRanch, a legal brothel in Nevada.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q3e739ab132",
  "kind": "yes/no",
  "text": "Claim: Joseph Smith founded Methodism along with the man who was also part of the revival movement in England and the Great Awakening in the United States.\n\nPassages:\n\n[John Wesley]\nJohn Wesley ( or ; 28 June [O.S. 17 June] 1703 2 March 1791) was an English Anglican cleric and theologian who, with his brother Charles and fellow cleric George Whitefield, founded Methodism.\n\n[United Methodist Church]\nThe UMC traces its roots back to the revival movement of John and Charles Wesley in England as well as the Great Awakening in the United States.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q9bff8e77f0",
  "kind": "yes/no",
  "text": "Claim: A Shinee group member's first studio album sold 4.5 million copies and was distributed by KT Music.\n\nPassages:\n\n[Kim Jong-hyun (singer)]\nKim Jong-hyun (born April 8, 1990), better known by the mononym Jonghyun, is a South Korean singer-songwriter, and radio host.\n\n[Shinee]\nThe group is composed of five members: Onew, Jonghyun, Key, Minho and Taemin.\n\n[She Is]\nShe Is (Hangul: 좋아 ; RR: \"Joh ah \" \"good\") is the first studio album by South Korean singer-songwriter Jonghyun, released on May 24, 2016 by S.M. Entertainment and distributed by KT Music.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4528e01d19",
  "kind": "yes/no",
  "text": "Claim: Italian Ann-Marie MacDonald is not from the same country as another literary figure. The other literary figure wrote \"The Sign in Sidney Brustein's Window\".\n\nPassages:\n\n[Ann-Marie MacDonald]\nAnn-Marie MacDonald (born October 29, 1958) is a Canadian playwright, novelist, actress and broadcast host who lives in Toronto, Ontario, Canada.\n\n[Lorraine Hansberry]\nLorraine Vivian Hansberry (May 19, 1930 – January 12, 1965) was an African-American playwright and writer.\n\n[The Sign in Sidney Brustein's Window]\nThe Sign in Sidney Brustein's Window is the second and last staged play by playwright Lorraine Hansberry, author of \"A Raisin in the Sun\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb2ca776f5a",
  "kind": "yes/no",
  "text": "Claim: Atomweight class belongs to mixed martial arts.\n\nPassages:\n\n[Liz McCarthy (fighter)]\nLiz McCarthy is an American mixed martial artist who competes in the Atomweight division.\n\n[Atomweight (MMA)]\nThe atomweight division in mixed martial arts generally refers to competitors weighing at or less than 105 lb .",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qfc5a2fba46",
  "kind": "yes/no",
  "text": "Claim: Sixpence None the Richer is a rock band and not the band who sand A Heavy Abacus.\n\nPassages:\n\n[A Heavy Abacus]\n\"A Heavy Abacus\" is the fifth and final single from Welsh alternative rock band The Joy Formidable's debut album \"The Big Roar\", released in July 2011.\n\n[The Joy Formidable]\nThe Joy Formidable is a Welsh alternative rock band, formed in 2007 in North Wales and currently based in London, England.\n\n[Sixpence None the Richer]\nSixpence None the Richer (also known as Sixpence) is an American alternative Christian rock band that formed in New Braunfels, Texas, eventually settling in Nashville, Tennessee.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4101c8a35f",
  "kind": "yes/no",
  "text": "Claim: Five Nights at Freddy's 2, from summer 2002, is the sequel to a game where a player must act as a night security guard, which was a new intellectual property released in 2014.\n\nPassages:\n\n[Five Nights at Freddy's (video game)]\nThe game centers around a fictional pizza restaurant called \"Freddy Fazbear's Pizza\", where the player must act as a night security guard, defending themselves from the malfunctioning, haunted animatronic characters by tracking their movement through the facility using security cameras.\n\n[2014 in video gaming]\nIn addition, it saw the release of many new intellectual properties, such as \"Destiny\", \"Five Nights at Freddy's,\" \"Sunset Overdrive\", \"Titanfall\", \"The Evil Within\" and \"Watch Dogs\".\n\n[Five Nights at Freddy's 2]\nIt is the second game in the \"Five Nights at Freddy's\" series, and is chronologically set before the events of the first game.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8314f9b838",
  "kind": "yes/no",
  "text": "Text: Maybe if we didn’t comment on things that don’t concern us, the world would be a happier place?? But what do I know🤷🏻‍♀️",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q16142106a7",
  "kind": "yes/no",
  "text": "Claim: Gevork Minaskanian and George Stambolian were both Western Armenian educators and writers.\n\nPassages:\n\n[George Stambolian]\nGeorge Stambolian (born April 10, 1938 – December 22, 1991, New York City) was an American educator, writer, and editor of Armenian descent. Stambolian was a key figure in the early gay literary movement that came out of New York during the 1960s and 1970s.\n\n[Gevork Minaskanian]\nDr. Minaskanian is the inventor and author of over 50 patents and publications in various fields of organic and medicinal chemistry.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qd3b2b158f3",
  "kind": "yes/no",
  "text": "Claim: Pinnacle Airlines Flight 3701 was headed to an airport when it crashed. That airport is farther east than Cheyenne Regional Airport.\n\nPassages:\n\n[Pinnacle Airlines Flight 3701]\nIt was an overnight repositioning flight with no passengers from Little Rock, Arkansas, U.S. to Minneapolis–Saint Paul International Airport, U.S. Both crew members were killed.\n\n[Cheyenne Regional Airport]\nCheyenne Regional Airport (IATA: CYS, ICAO: KCYS, FAA LID: CYS) (Jerry Olson Field) is a civil-military airport a mile north of downtown Cheyenne, in Laramie County, Wyoming.\n\n[Minneapolis–Saint Paul International Airport]\nMinneapolis–Saint Paul International Airport (IATA: MSP, ICAO: KMSP, FAA LID: MSP) , also known as Wold–Chamberlain Field, is a joint civil-military public use international airport.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q0e12e0e118",
  "kind": "yes/no",
  "text": "Claim: American singer-songwriter Roy Orbison, known as \"the Caruso of Rock\", recorded on the Monument Records label and had hits such as \"Pretty One,\" and \"Uptown\".\n\nPassages:\n\n[Roy Orbison]\nRoy Kelton Orbison (April 23, 1936 – December 6, 1988) was an American singer-songwriter known for his distinctive, impassioned voice, complex song structures, and dark emotional ballads.\n\n[Early Orbison]\nEarly Orbison is an album recorded by Roy Orbison on the Monument Records label at their studios in Hendersonville, Tennessee and released in 1964. Essentially a compilation of songs from his first two Monument albums, it is most noteworthy for containing \"Pretty One\", the \"B\" side of Orbison's second Monument single, \"Uptown\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qbe8491823c",
  "kind": "yes/no",
  "text": "Claim: 1614 is the founding year of the public research university in the Amsterdam, where Jan Borgman was a professor from 1968 to 1988.\n\nPassages:\n\n[University of Groningen]\nThe University of Groningen (abbreviated as UG; Dutch: \"Rijksuniversiteit Groningen\" , abbreviated as \"RUG\") is a public research university in the city of Groningen in the Netherlands. The university was founded in 1614 and is one of the oldest universities in the Netherlands as well as one of its largest.\n\n[Jan Borgman]\nJan Borgman (born 30 November 1929) is a Dutch astronomer and university administrator. He was professor of astronomical observation technique at the University of Groningen from 1968 to 1988.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q814c185452",
  "kind": "yes/no",
  "text": "Claim: The High Sheriff changes every March for the role of William Vere Reeve King-Fane since 1991.\n\nPassages:\n\n[High Sheriff of Lincolnshire]\nThe High Sheriff changes every March.\n\n[William Vere Reeve King-Fane]\nColonel William Vere Reeve King-Fane, JP, DL (born Fane; 29 October 1868 – 5 November 1943) was an English local politician, magistrate and landowner, who served as Vice-Chairman of Kesteven County Council and High Sheriff of Lincolnshire.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qb38127922d",
  "kind": "yes/no",
  "text": "Text: Wizkid is the king, ok lol",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q8718251d6c",
  "kind": "yes/no",
  "text": "Claim: A British author wrote the books the 2000 TV series The Jewel in the Crown were based on. Both he and the writer of Amédée, or How to Get Rid of It, are playwrights that lived during the same time period.\n\nPassages:\n\n[Eugène Ionesco]\nEugène Ionesco (born Eugen Ionescu, ] ; 26 November 1909 – 28 March 1994) was a Romanian-French playwright who wrote mostly in French, and one of the foremost figures of the French Avant-garde theatre.\n\n[Paul Scott (novelist)]\nPaul Mark Scott (25 March 19201 March 1978) was an English novelist, playwright, and poet, best known for his monumental tetralogy \"The Raj Quartet.\"\n\n[Amédée, or How to Get Rid of It]\nAmédée, or How to Get Rid of It (French: \"Amédée ou comment s'en débarrasser\" ) is a play written by Eugène Ionesco in 1954 based on his earlier short story entitled \"Oriflamme\".\n\n[The Jewel in the Crown (TV series)]\nThe Jewel in the Crown is a 1984 British television serial about the final days of the British Raj in India during and after World War II, based upon the \"Raj Quartet\" novels (1965–75) by British author Paul Scott.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q8cc23fb90f",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "My ancestors spoke about a lot of true things",
   "“tit for tat, butter for fat, you kill my dog, i eat your cat” is a liberian proverb for “an eye for an eye”. my ancestors were spittin’"
  ]
 },
 {
  "qid": "q02e73d7c24",
  "kind": "yes/no",
  "text": "Claim: Mickey Gilley founded the honky tonk that is at the center of John Travolta's third major acting role.\n\nPassages:\n\n[Gilley's Club]\nGilley's was a bar/honky tonk founded in 1971 by country singer Mickey Gilley in Pasadena, Texas.\n\n[Urban Cowboy]\nIt was John Travolta's third major acting role after \"Saturday Night Fever\" and \" Grease\". Much of the action centers around activities at Gilley's Club, a honky tonk in Pasadena, Texas.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qb93f441e32",
  "kind": "yes/no",
  "text": "Post: Amazing show last night from @TheMovielifeNYC (w/ special guest @brettromnes!) - thanks @vinniecaruana, @BrandonReilly and Navetta Bros. !",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qbfc374c636",
  "kind": "yes/no",
  "text": "Text: ITS COMING HOOOOOME",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q92d0265e34",
  "kind": "yes/no",
  "text": "Claim: The college which the Charleston architect, hired to remodel Louis Gourd House, taught at was founded in 1770.\n\nPassages:\n\n[Louis Gourd House]\nWhen the building was acquired by Mr. and Mrs. Louis Gourd in 1939, they quickly hired Charleston architect Albert Simons to plan to remodeling of the building.\n\n[Albert Simons]\nAs a professor at the College of Charleston for over 20 years, he started the School of the Arts whose building is named after him and is honored yearly through the Simons Medal of Excellence.\n\n[College of Charleston]\nFounded in 1770 and chartered in 1785, it is the oldest college in South Carolina, the 13th oldest institution of higher learning in the United States, and the oldest municipal college in the country.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q6a3d1f3da4",
  "kind": "yes/no",
  "text": "Claim: Dancer Gregory Hines, who died on August 9, 2003, appeared in White Nights.\n\nPassages:\n\n[White Nights (1985 film)]\nWhite Nights is a 1985 American drama film directed by Taylor Hackford and choreographed by Twyla Tharp and stars Mikhail Baryshnikov, Gregory Hines, Jerzy Skolimowski, Helen Mirren and Isabella Rossellini.\n\n[Gregory Hines]\nGregory Oliver Hines (February 14, 1946 – August 9, 2003) was an American dancer, actor, singer, and choreographer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q20cba1e9d3",
  "kind": "yes/no",
  "text": "Post: im ollie im 5'8 and i think my 5'7 boyfriend is short",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q4c77212de5",
  "kind": "yes/no",
  "text": "Claim: Carl Maria Friedrich Ernst von Weber was born earlier than Charles Gounod.\n\nPassages:\n\n[Charles Gounod]\nCharles-François Gounod (] ; 17 June 181817 or 18 October 1893) was a French composer, best known for his \"Ave Maria,\" based on a work by Bach, as well as his opera \"Faust\".\n\n[Carl Maria von Weber]\nCarl Maria Friedrich Ernst von Weber (18 or 19 November 1786 5 June 1826) was a German composer, conductor, pianist, guitarist and critic, and was one of the first significant composers of the Romantic school.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa60bce2a26",
  "kind": "yes/no",
  "text": "Claim: Todd Boehly's former position at the firm where Mark Walter is the CEO was president.\n\nPassages:\n\n[Eldridge Industries]\nEldridge Industries, LLC is a Private equity investment holdings firm owned by Todd Boehly, the former president of Guggenheim Partners.\n\n[Guggenheim Partners]\nThe firm's CEO is Mark Walter.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q76f4459e4b",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "just found ive been walking on a broken foot for the past 6 months 🤪🤪🤪",
   "Just found out I've been walking on a broken foot for the past six months :( may have to get surgery again"
  ]
 },
 {
  "qid": "q4f58fa18f7",
  "kind": "yes/no",
  "text": "Claim: It was reported that Hess took an illegal flight to Scotland in May 1941. This report was the reason that the editor of the publication, that was published by Fredric Warburg, stopped serving Hitler in 1941.\n\nPassages:\n\n[Mein Kampf]\nThe book was edited by Hitler's deputy Rudolf Hess.\n\n[Fredric Warburg]\nOther notable publications included \"The Third Eye\" by Lobsang Rampa, Pierre Boulle's \"The Bridge over the River Kwai\", Adolf Hitler's \"Mein Kampf\" and William Shirer's \"The Rise and Fall of the Third Reich\".\n\n[Karlheinz Pintsch]\nIt fell to him to report Hess's illegal May 1941 flight to Scotland to Hitler and his recollections and notes have been the subject of debate by historians.\n\n[Rudolf Hess]\nAppointed Deputy Führer to Adolf Hitler in 1933, he served in this position until 1941, when he flew solo to Scotland in an attempt to negotiate peace with the United Kingdom during World War II. He was taken prisoner and eventually was convicted of crimes against peace, serving a life sentence until his suicide.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q6d7be99cab",
  "kind": "yes/no",
  "text": "Claim: A women's cricket team based in Sydney, Australia featured an Australian sportswoman named Ellyse Alexander Perry. Ashleigh Gardner played for this team as well.\n\nPassages:\n\n[Ellyse Perry]\nEllyse Alexandra Perry (born 3 November 1990) is an Australian sportswoman who made her debut for both the Australian cricket and the Australian women's national soccer team at the age of 16.\n\n[Ashleigh Gardner]\nAshleigh Gardner (born 15 April 1997) is an Australian cricketer who plays for New South Wales Breakers in the Women's National Cricket League and Sydney Sixers in the Australian Women's Big Bash League.\n\n[Sydney Sixers (WBBL)]\nThe Sydney Sixers WBBL team is a women's cricket team based in Sydney, Australia, that competed in the inaugural women's Twenty20 Women's Big Bash League commenced in December, 2015.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa04b6ba6a1",
  "kind": "yes/no",
  "text": "Claim: Pete Mount was the father of the American Basketball Player who was the first high school athlete on the cover of American Basketball Association.\n\nPassages:\n\n[Rick Mount]\nHe was the first high school athlete to be featured on the cover of \"Sports Illustrated\".\n\n[Pete Mount]\nPete was the father of American Basketball Association player Rick Mount.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5912836a4e",
  "kind": "yes/no",
  "text": "Claim: El Paso International Airport is further from their town than Grand Forks International.\n\nPassages:\n\n[El Paso International Airport]\nEl Paso International Airport (IATA: ELP, ICAO: KELP, FAA LID: ELP) is a public airport four miles (6 km) northeast of downtown El Paso, in El Paso County, Texas, United States.\n\n[Grand Forks International Airport]\nGrand Forks International Airport (IATA: GFK, ICAO: KGFK, FAA LID: GFK) is a public airport five miles (8 km) northwest of Grand Forks, in Grand Forks County, North Dakota.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc38a4750d5",
  "kind": "yes/no",
  "text": "Claim: Steven Jackson, an American running back, played for Oregon State and was coached by Paul Boudreau.\n\nPassages:\n\n[Steven Jackson]\nSteven Rashad Jackson (born July 22, 1983) is a former American football running back.\n\n[Paul Boudreau]\nPaul T. Boudreau (born December 30, 1949) is an American football coach who last served as offensive line coach for the Los Angeles Rams of the National Football League (NFL). Boudreau’s stellar offensive lines over the years have helped pave the way for five running backs to top the 10,000-yard career rushing mark, including Barry Sanders, Curtis Martin, Thurman Thomas, Fred Taylor and Steven Jackson.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qe87528aa9a",
  "kind": "yes/no",
  "text": "Claim: The quarterly Sports Collectors Digest is one magazine that published papers more often than another magazine. The other magazine had Ole Anthony as an editor.\n\nPassages:\n\n[Ole Anthony]\nAnthony was the editor of \"The Wittenburg Door\", a magazine of Christian satire.\n\n[The Wittenburg Door]\nThe Wittenburg Door, sometimes known as simply The Door, was a Christian satire and humor magazine, published bimonthly by the non-profit Trinity Foundation based in Dallas, Texas.\n\n[Sports Collectors Digest]\nSports Collectors Digest (SCD) is an American advertising weekly paper published at Iola, Wisconsin.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf7458712ae",
  "kind": "yes/no",
  "text": "Claim: The rock band Sugar Ray began as a funk metal band, while the band Das Damen was considered alternative rock.\n\nPassages:\n\n[Das Damen]\nDas Damen was an alternative rock band from New York City, United States, formed in 1984.\n\n[Sugar Ray]\nThe band, starting off more as a funk metal band, gained mainstream fame in 1997 with their release of the song \"Fly\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q7926465aa8",
  "kind": "yes/no",
  "text": "Claim: A noteworthy performer produced by All for One Theater was born in Notts County, Montana.\n\nPassages:\n\n[Tom Hewitt (actor)]\nTom Hewitt (born c. 1957) is an American actor and Broadway stage performer, and a native of Victor, Montana.\n\n[All for One Theater]\nNoteworthy performers whom AFO has produced include Tom Hewitt, Deb Margolin, Leslie Jordan, Annabelle Gurwitch, and Bill Bowers.\n\n[Victor, Montana]\nVictor is a census-designated place (CDP) in Ravalli County, Montana, United States.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q36f0781132",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "How does one find motivation to do basically anything? Asking for a friend.",
   "\"How does somebody find motivation to do basically anything? I haven't had motivation in ages.\""
  ]
 },
 {
  "qid": "q12b2b80145",
  "kind": "yes/no",
  "text": "Claim: The American honky tonk country band, whose first studio album was Honky Tonks and Cheap Motels, is based in Flint, Michigan, United States.\n\nPassages:\n\n[Honky Tonks and Cheap Motels]\nHonky Tonks and Cheap Motels is the first studio album by Whitey Morgan and the 78's.\n\n[Whitey Morgan and the 78's]\nWhitey Morgan and the 78's are an American honky tonk country band, based in Flint, Michigan, United States.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q8d14fbbe06",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Lil Pump is the Nelson Mandela of our generation",
   "Lil Pump is not the Nelson Mandela of our generation"
  ]
 },
 {
  "qid": "q831b00f094",
  "kind": "yes/no",
  "text": "Claim: An American reality-based nontraditional court show that debuted in syndication on September 26,2011, is produced by an Emmy winning producer and actor, who played football.\n\nPassages:\n\n[Matt Battaglia]\nMatteo Martin \"Matt\" Battaglia (born September 25, 1965) is an Emmy winning producer, American actor and former American football player.\n\n[Last Shot with Judge Gunn]\nLast Shot with Judge Gunn is an American reality-based nontraditional court show that debuted in syndication on September 26, 2011. The series is presented by Mary Ann Gunn and distributed by Trifecta Entertainment, with Peter Brennan, Matt Battaglia, and George Jones serving as executive producers on this series, with Lisa Lew as Co-Executive Producer, and Justin Page and Terry Powell as Supervising Producers.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q796d0409d1",
  "kind": "yes/no",
  "text": "Claim: The radio station which played oldies from artists such as Leopoldo Dante Tévez, broadcasted in Spanish throughout North America between 1979 and 1995.\n\nPassages:\n\n[Caricia]\nCaricia was a radio station on XM Satellite Radio channel 93 and DirecTV channel 875. In addition, the channel is available only to DirecTV subscribers who subscribe to the Spanish language programming package.\n\n[Leo Dan]\nLeopoldo Dante Tévez (born June 1, 1942), known as Leo Dan, is an Argentine composer and singer born in Villa Atamisqui, Santiago del Estero Province.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qdc03462c7e",
  "kind": "yes/no",
  "text": "Claim: This military leader led the military coup to remove Carlos Prío Socarrás from office. The Greek President served as inspiration for the composer of the song Quizás, Quizás, Quizás.\n\nPassages:\n\n[Carlos Prío Socarrás]\nCarlos Prío Socarrás (July 14, 1903 – April 5, 1977) was the President of Cuba from 1948 until he was deposed by a military coup led by Fulgencio Batista on March 10, 1952, three months before new elections were to be held.\n\n[Quizás, Quizás, Quizás]\nFarrés also received much help and inspiration for his lyrics from Cuban First Lady, Mary Tarrero-Serrano.\n\n[Fulgencio Batista]\nFulgencio Batista y Zaldívar (] ; born Rubén Zaldívar; January 16, 1901 – August 6, 1973) was the elected President of Cuba from 1940 to 1944, and U.S.-backed dictator from 1952 to 1959, before being overthrown during the Cuban Revolution.\n\n[Mary Tarrero-Serrano]\nShe was the second wife of Cuban President, Carlos Prio, who was overthrown by Fulgencio Batista in a military coup.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 }
]
