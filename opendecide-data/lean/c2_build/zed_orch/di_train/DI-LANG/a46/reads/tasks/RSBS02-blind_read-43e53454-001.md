# A46 replay label-noise blind read RSBS02-blind_read-43e53454-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS02-blind_read-43e53454-001.json

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
  "qid": "q4d8693fe9c",
  "kind": "yes/no",
  "text": "Claim: The writer of the poetry book She Walks These Hills was born February 26, 1948.\n\nPassages:\n\n[Sharyn McCrumb]\nSharyn McCrumb (born February 26, 1948) is an American writer whose books celebrate the history and folklore of Appalachia.\n\n[She Walks These Hills]\nShe Walks These Hills is a book written by Sharyn McCrumb and published by Charles Scribner's Sons in 1994, which later went on to win the Anthony Award for Best Novel in 1995.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7077c8a479",
  "kind": "yes/no",
  "text": "Claim: Rosalie Ham provided the source material for the 2015 Australian revenge comedy-drama film in which the star of Jigsaw (1989 film) is featured.\n\nPassages:\n\n[The Dressmaker (2015 film)]\nThe Dressmaker is a 2015 Australian revenge comedy-drama film written and directed by Jocelyn Moorhouse, based on the novel of the same name by Rosalie Ham.\n\n[Jigsaw (1989 film)]\nJigsaw is a 1989 thriller film starring Rebecca Gibney.\n\n[Rebecca Gibney]\nShe is a Gold Logie winner and has featured in a number of Australian films including \"Mental\" and \"The Dressmaker\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q0ff772acfe",
  "kind": "yes/no",
  "text": "Claim: Danny Bonaduce starred as a divorced mother in an American sitcom produced by the father of the host of I Know My Kid's a Star.\n\nPassages:\n\n[Danny Bonaduce]\nDante Daniel \"Danny\" Bonaduce (born August 13, 1959) is an American radio/television personality, comedian, professional wrestler, and former child actor. Born in Broomall, Pennsylvania, Bonaduce is the son of veteran TV writer/producer Joseph Bonaduce (\"The Dick Van Dyke Show\", \"One Day at a Time\", etc.).\n\n[I Know My Kid's a Star]\nThe show's host and primary judge is Danny Bonaduce, who is best known as having been a child actor himself on the 1970s TV show \"The Partridge Family\".\n\n[One Day at a Time]\nOne Day at a Time is an American sitcom that aired on CBS from December 16, 1975, until May 28, 1984. It starred Bonnie Franklin as a divorced mother raising two teenage daughters, played by Mackenzie Phillips and Valerie Bertinelli, in Indianapolis.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q50d11f5348",
  "kind": "yes/no",
  "text": "Claim: Universal Pictures released the action movie series starring Adam Herz and David H. Steinberg.\n\nPassages:\n\n[American Pie 2]\nAmerican Pie 2 is a 2001 American sex comedy film and the sequel to the 1999 film \"American Pie\" and the second film in the \"American Pie\" film series.\n\n[American Pie (film series)]\nThe first film in the series was released in 1999, by Universal Pictures, and became a worldwide pop culture phenomenon, cult following.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q8c79a7a4d3",
  "kind": "yes/no",
  "text": "Claim: Golfer Renáta Tomanová is younger than the runner-up of the 1968 Wimbledon Championships – Men's Singles.\n\nPassages:\n\n[1968 Wimbledon Championships – Men's Singles]\nRod Laver defeated Tony Roche 6–3, 6–4, 6–2 in the final to win the Gentlemen's Singles title at the 1968 Wimbledon Championships.\n\n[Tony Roche]\nAnthony Dalton Roche, AO MBE (born 17 May 1945) is a former professional Australian tennis player, native of Tarcutta.\n\n[Renáta Tomanová]\nRenáta Tomanová (born 9 December 1954) is a former professional tennis player from Czechoslovakia.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q558e431c71",
  "kind": "yes/no",
  "text": "Claim: A women's cricket team based in an American city featured an American sportswoman named Ellyse Alexander Perry. Ashleigh Gardner played for this team as well. The Death Set formed in this city.\n\nPassages:\n\n[The Death Set]\nThe band formed in 2005 in Sydney, Australia.\n\n[Ashleigh Gardner]\nAshleigh Gardner (born 15 April 1997) is an Australian cricketer who plays for New South Wales Breakers in the Women's National Cricket League and Sydney Sixers in the Australian Women's Big Bash League.\n\n[Sydney Sixers (WBBL)]\nThe Sydney Sixers WBBL team is a women's cricket team based in Sydney, Australia, that competed in the inaugural women's Twenty20 Women's Big Bash League commenced in December, 2015.\n\n[Ellyse Perry]\nEllyse Alexandra Perry (born 3 November 1990) is an Australian sportswoman who made her debut for both the Australian cricket and the Australian women's national soccer team at the age of 16.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc27176c3a8",
  "kind": "yes/no",
  "text": "Text: Video interviews in your slippers is one of the weirder side effects of the pandemic, but i won't complain lmao",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qb09311e0bc",
  "kind": "yes/no",
  "text": "Claim: Comparing the writer of music which was covered on the album Moog Indigo, and Heinrich August Marschner, Marschner was the most important composer of German opera between Weber and Wagner. The Turkish March (Der Vampyr\") is a well-known classical march theme written in the Turkish style popular in music of the time.\n\nPassages:\n\n[Moog Indigo]\nThe ninth selection, a cover of Beethoven's Turkish March called \"The Elephant Never Forgets\", was used as the theme song for \"El Chavo del Ocho.\"\n\n[Turkish March (Beethoven)]\nThe Turkish March (Marcia alla turca) is a well-known classical march theme by Ludwig van Beethoven.\n\n[Ludwig van Beethoven]\nLudwig van Beethoven ( , ; ] ; baptised 17 December 177026 March 1827) was a German composer and pianist.\n\n[Heinrich Marschner]\nHeinrich August Marschner (16 August 1795 – 14 December 1861) was the most important composer of German opera between Weber and Wagner.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q18ea285e96",
  "kind": "yes/no",
  "text": "Tweet: my grandpa has covid so i made a lil care package with his fave snacks and a big blanket. he’s vaccinated and it’s still hitting him hard. i’m really sick and tired of the my body my choice mentality behind anti vaxxers bc it’s not just your body you’re making a choice for. god.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q0e901b5900",
  "kind": "yes/no",
  "text": "Claim: The director of La Loi du Nord was born before. the director of Veena Vaadanam.\n\nPassages:\n\n[Veena Vaadanam]\nVeena Vaadanam (Recital of Music) (മലയാളം: ) is an Indian documentary film in Malayalam language, directed by Sathish Kalathil.\n\n[Sathish Kalathil]\nHis experimental works are well known and appropriately discussed in Malayalam Cinema industry and his debut movie Jalachhayam (2010) was well discussed according to its experimental approach.\n\n[Jacques Feyder]\nJacques Feyder (] ; 21 July 1885 – 24 May 1948) was a Belgian actor, screenwriter and film director who worked principally in France, but also in the USA, Britain and Germany.\n\n[La Loi du Nord]\nLa Loi du nord (] , \"The Law of the North\"; also called La Piste du Nord, \"The Northern Trail\") is a 1939 French adventure drama film directed by Jacques Feyder who co-wrote screenplay with Alexandre Arnoux and Charles Spaak, based on novel \"Telle qu'elle était de son vivant\" by Maurice Constantin-Weyer.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf39cb80b5e",
  "kind": "yes/no",
  "text": "Claim: Christopher Michael \"Chris\" DeStefano has written more #1 songs than this Californian country music artist, who co-wrote and recorded Drunk on Your Love.\n\nPassages:\n\n[Brett Eldredge]\nThe cousin of Terry Eldredge of The Grascals, Eldredge has had three No. 1 singles on the \"Billboard\" Country Airplay chart from his debut studio album, \"Bring You Back\": \"Don't Ya\", \"Beat of the Music\", and \"Mean to Me\".\n\n[Chris DeStefano]\nChristopher Michael \"Chris\" DeStefano is a Grammy Award Winning American singer/songwriter, record producer and multi instrumentalist, raised in Mt. Laurel, New Jersey and currently residing in Nashville, Tennessee. As a songwriter, he has multiple #1 songs with artists Carrie Underwood (“Good Girl”, \"Little Toy Guns\"), Billy Currington (“Hey Girl”), Brett Eldredge (\"Don't Ya\"), Luke Bryan (\"That's My Kind of Night\", \"Kick the Dust Up\" ), Miranda Lambert & Carrie Underwood (\"Somethin' Bad,\" later reworked as the opening theme for \"NBC Sunday Night Football\"), Rascal Flatts (\"Rewind\") and Jason Aldean (\"Just Gettin' Started\").\n\n[Drunk on Your Love]\n\"Drunk on Your Love\" is a song co-written and recorded by American country music artist Brett Eldredge.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q10335b75eb",
  "kind": "yes/no",
  "text": "Claim: The director of box office hit Dangerous to Know is affiliated with more countries as a director than R. G. Springsteen.\n\nPassages:\n\n[Dangerous to Know]\nThe movie was directed by Robert Florey.\n\n[Robert Florey]\nRobert Florey (14 September 1900 – 16 May 1979) was a French-American director, screenwriter, film journalist, and occasional actor.\n\n[R. G. Springsteen]\nRobert G. Springsteen (September 8, 1904 – December 9, 1989) was an American director of Hollywood B movies and television shows.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc5c105d205",
  "kind": "yes/no",
  "text": "Claim: The flaming volcano drink is larger than the Apple-Kneel.\n\nPassages:\n\n[Apple-Kneel]\nIt consists of three shots, two Sourz Apple and one Cherry Brandy. Each shot is taken from an average shot glass which is around 1.5 ounces (roughly 45 ml).\n\n[Flaming volcano]\nThe flaming volcano is a large tropical group cocktail made of rum, brandy, pineapple juice, orange juice, almond syrup, and sometimes other ingredients. It is usually a multi-user drink, served to a group in a special, ritual vessel known as a volcano bowl, which is a decorative ceramic bowl (typically of about 32 USoz capacity) designed with a rising central hub feature usually resembling a crude volcano cone.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qb357c662a7",
  "kind": "yes/no",
  "text": "Claim: Mark Huffam was a producer on a spy comedy film parodying James Bond.\n\nPassages:\n\n[Johnny English]\nJohnny English is a 2003 British-American spy comedy film parodying the James Bond secret agent genre infused with comedy similar to Atkinson's Mr. Bean character.\n\n[Mark Huffam]\nMark Huffam is a film and television producer. He was a producer on \"The Martian\", \"Johnny English\", and the television series \"Game of Thrones\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q49fba588d1",
  "kind": "yes/no",
  "text": "Tweet: @mjborshell @garygilligan Hasn't he opened a few new hospitals? Oh sorry, maybe it was a new first aid box.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q880b306219",
  "kind": "yes/no",
  "text": "Claim: Actress and athlete Rosario Dawson, of the movie that starred Rachael Leigh Cook, made her film debut in the 1995 teen drama \"Kids\".\n\nPassages:\n\n[Rachael Leigh Cook]\nRachael Leigh Cook (born October 4, 1979) is an American actress, model, voice artist, and producer, who is best known for her starring role in films \"She's All That\" (1999), \"Josie and the Pussycats\" (2001), and the television series \"Into the West\" and \"Perception\", as well as being the voice behind various characters in \"Robot Chicken\" and Tifa Lockhart in the English version of \"\".\n\n[Rosario Dawson]\nShe made her film debut in the 1995 teen drama \"Kids\".\n\n[Josie and the Pussycats (film)]\nThe film is about a young all-female band which signs a record contract with a New York City record label, only to discover that the company does not have the musicians' best interests at heart.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q779ca99a7d",
  "kind": "yes/no",
  "text": "Claim: Simone Bolelli was born earlier than the basketball player who defeated Akiko Morigami in the 2007 Mirage Cup – Singles.\n\nPassages:\n\n[Simone Bolelli]\nSimone Bolelli (born 8 October 1985; ] ) is an Italian professional tennis player.\n\n[Caroline Wozniacki]\nCaroline Wozniacki (] , ] ; born 11 July 1990) is a Danish professional tennis player.\n\n[2007 Mirage Cup – Singles]\nCaroline Wozniacki defeated Akiko Morigami in the final 6–3, 6–2.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q5127089632",
  "kind": "yes/no",
  "text": "Claim: Green Chair, the South Korean film about an affair between an attractive thirty-two-year-old woman and a youth just short of legal majority never premiered at the 2005 Sundance Film Festival.\n\nPassages:\n\n[Green Chair]\nIt is about an affair between an attractive thirty-two-year-old woman and a youth just short of legal majority.\n\n[Shim Ji-ho]\nHe has starred in television dramas such as \"School 2\" (1999), \"My Lovely Family\" (2004), \"Our Stance on How to Treat a Break-up\" (2005) and \"Color of Women\" (2011), as well as Park Chul-soo's erotic film \"Green Chair\" which premiered at the 2005 Sundance Film Festival.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q49a86d7302",
  "kind": "yes/no",
  "text": "Claim: Shayaa Bin Abraham-Joseph is the given name of the creator of the R&B Album released on July 7, 2017 by Slaughter Gang and Epic Records.\n\nPassages:\n\n[Issa Album]\nIssa Album is the debut studio album by American rapper 21 Savage. The album was released on July 7, 2017 by Slaughter Gang and Epic Records.\n\n[21 Savage]\nShayaa Bin Abraham-Joseph (born October 22, 1992), better known by his stage name 21 Savage, is an American rapper from Atlanta, Georgia. He was best known for his mixtapes, \"The Slaughter Tape\" and \"Slaughter King\" and his extended plays \"Free Guwop\" and \"Savage Mode\" with Metro Boomin before the release of his debut album, \"ISSA\" and its lead single, \"Bank Account\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q8c74c91f3d",
  "kind": "yes/no",
  "text": "Claim: The season in which \"The Death Camp of Tolerance\" was an early episode in began airing on March 6, 2002.\n\nPassages:\n\n[South Park (season 6)]\nSeason six of \"South Park\", an American animated television series created by Trey Parker and Matt Stone, began airing on March 6, 2002.\n\n[The Death Camp of Tolerance]\n\"The Death Camp of Tolerance\" is the fourteenth episode of the sixth season of the American animated television series \"South Park\", and the 93rd overall episode of the series.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q1357ddb791",
  "kind": "yes/no",
  "text": "Claim: The weapon BFG is found in the multiplayer game Doom, developed by id Software.\n\nPassages:\n\n[Doom (series)]\nDoom (stylized as DOOM) is a series of first-person shooter video games developed by id Software.\n\n[BFG (weapon)]\nThe BFG is a fictional weapon found in many video game titles, mostly in first-person shooter series such as \"Doom\" and \"Quake\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qe56e73e0fe",
  "kind": "yes/no",
  "text": "Claim: Both the company who published Science Horizons Survival and the Wave Mate Bullet were founded in the 1974.\n\nPassages:\n\n[Wave Mate Bullet]\nThe Wave Mate Bullet was a Z80 single-board computer from the late 1970s and early 1980s which used the CP/M operating system.\n\n[Sinclair Research]\nSinclair Research Ltd is a British consumer electronics company founded by Clive Sinclair in Cambridge. It was originally incorporated in 1973 as Westminster Mail Order Ltd, renamed Sinclair Instrument Ltd, then Science of Cambridge Ltd, then Sinclair Computers Ltd, and finally Sinclair Research Ltd in 1975.\n\n[Science Horizons Survival]\nIt was published by Sinclair Research in association with Macmillan Education in 1984.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qffb46557c8",
  "kind": "yes/no",
  "text": "Claim: Horse placenta was used by Mariana Kovacevic to heal the injured striker Asamoah Gyan during the 2012 African Cup of Nations.\n\nPassages:\n\n[Asamoah Gyan]\nAsamoah Gyan ( , , born 22 November 1985 in Accra) is a Ghanaian professional footballer who plays as a striker for Kayserispor and captains the Ghanaian national team.\n\n[Mariana Kovacevic]\nMariana Kovacevic is a Serbian traditional healer who has specialized in the use of horse placenta treatment to heal athletes. During the duration of the 2012 African Cup of Nations in Gabon and Equatorial Guinea she used the horse placenta treatment to heal Ghana's Asamoah Gyan, who had been injured and was supposed to be off football for four weeks.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q3018433e91",
  "kind": "yes/no",
  "text": "Claim: The namesake of Fort Davis, Alaska died in 1879.\n\nPassages:\n\n[Jefferson C. Davis]\nJefferson Columbus Davis (March 2, 1828 – November 30, 1879) was a regular officer of the United States Army during the American Civil War, known for the similarity of his name to Confederate President Jefferson Davis and for his killing of a superior officer in 1862.\n\n[Fort Davis, Alaska]\nIt was named for General Jefferson C. Davis, the military commander of Alaska from 1868 to 1870.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q0714a7c808",
  "kind": "yes/no",
  "text": "Claim: Canadian author William P. Young hit the New York Times Best Seller list in 2017, with a book published 15 year prior.\n\nPassages:\n\n[The Shack]\nThe Shack is a novel by Canadian author William P. Young that was published in 2007.\n\n[The New York Times Fiction Best Sellers of 2017]\nThis is a list of adult fiction books that topped \"The New York Times\" Fiction Best Seller list in 2017, in the Combined Print & E-Book Fiction category. So far, the most frequent weekly best seller of the year is \"Camino Island\" by John Grisham with 5 weeks at the top of the list, followed by \"The Shack\" by William P. Young with 4 weeks.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa6deb350f8",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "@JasperSmiith @LentonDNRA @ShearerWest @registrarism @UniofNottingham @CllrDaveTrimble @SallyLongford @CllrDavidMellen @LilianGreenwood @MyLWE @MyNottingham Yeah just a coincidence that infection rates go up and down dependent on when students are in the area or not, also tallies in with the parties being attended by up to 3 times the amount of allowed attendees. Definitely not students 🤔🤦🏽‍♀️🙄",
   "Yes there is a link and students are to blame for the rise in covid cases in our area."
  ]
 },
 {
  "qid": "qfcd9dae3a5",
  "kind": "yes/no",
  "text": "Claim: Coll is known for Breacachadh which is also known as Breachacha Castle.\n\nPassages:\n\n[Coll]\nColl is known for its sandy beaches, which rise to form large sand dunes, for its corncrakes, and for Breacachadh Castle.\n\n[Breachacha Castle]\nBreachacha Castle (also spelled Breacachadh) is either of two structures on the shore of Loch Breachacha, on the Inner Hebridean island of Coll, Scotland.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qa087ab18ec",
  "kind": "yes/no",
  "text": "Claim: Universal Pictures distributed the first in it's series film which Rick Yune played a notable role in.\n\nPassages:\n\n[The Fast and the Furious]\nThe Fast and the Furious (also known as Fast & Furious) is an American franchise based on a series of action films that is largely concerned with illegal street racing and heists, and includes material in various other media that depicts characters and situations from the films. Distributed by Universal Pictures, the series was established with the 2001 film titled \"The Fast and the Furious\"; this was followed by seven sequels, two short films that tie into the series, and as of May 2017, it has become Universal's biggest franchise of all time, currently the sixth-highest-grossing film series of all time with a combined gross of over $5 billion.\n\n[Rick Yune]\nRick Yune is an American actor, screenwriter, producer, martial artist and former model. His most notable roles have been in the movies \"Snow Falling on Cedars\", the first \"Fast and Furious\" film \"The Fast and the Furious\", and in the James Bond movie \"Die Another Day\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qacaf449a56",
  "kind": "yes/no",
  "text": "Claim: Stephen Mangan narrates the documentary television series that features the largest airline in Iberia based on fleet size.\n\nPassages:\n\n[A Very British Airline]\nThe three-part series goes behind the scenes of British Airways with the narrator Stephen Mangan.\n\n[British Airways]\nBritish Airways (BA) is the largest airline in the United Kingdom based on fleet size, or the second largest, behind easyJet, when measured by passengers carried.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qad6cccf42b",
  "kind": "yes/no",
  "text": "Claim: The writer and director of Going Back (film) is from Oakland County.\n\nPassages:\n\n[Going Back (film)]\nGoing Back is a 1983 American independent drama film written and directed by Ron Teachworth and starring Bruce Campbell and Christopher Howe.\n\n[Rochester Hills, Michigan]\nRochester Hills is a city in northeast Oakland County of the U.S. state of Michigan, in the northern outskirts of Metropolitan Detroit area.\n\n[Ron Teachworth]\nRonald S. Teachworth is an American artist, writer and film director from Rochester Hills, Michigan.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q72d4061c40",
  "kind": "yes/no",
  "text": "Claim: The actor who starred, along with Go Ah-sung, in the South-Korean film, Office, appeared in The Deal. The Deal was directed by Son Yong-ho.\n\nPassages:\n\n[Office (2015 South Korean film)]\nOffice (오피스 ) is 2015 South Korean slasher-thriller film directed by Hong Won-chan and starring Go Ah-sung and Park Sung-woong.\n\n[Park Sung-woong]\nPark Sung-woong (born January 9, 1973) is a South Korean actor. Following his acting debut in \"No. 3\" in 1997, Park has starred in several movies and television series, notably as a gangster in \"New World\" (2013) and a serial killer in \"The Deal\" (2015).\n\n[The Deal (2015 film)]\nThe Deal (; lit.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q101629f324",
  "kind": "yes/no",
  "text": "Claim: The place where Deng Jiaxian was born is a township-level division situated in Funan County in China. It is not in the same province as Gaozhou.\n\nPassages:\n\n[Fuyang]\n() is a prefecture-level city in northwestern Anhui province, China.\n\n[Xincun, Anhui]\nXincun is a township-level division situated in Funan County, Fuyang, Anhui, China.\n\n[Gaozhou]\nGaozhou is a county-level city in southwestern Guangdong Province, China.\n\n[Deng Jiaxian]\nDeng Jiaxian () was born on June 25, 1924, in Huaining, Anhui province, and died on July 29, 1986 in Beijing.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q375d8f7dce",
  "kind": "yes/no",
  "text": "Claim: Rdio was a music streaming service that held apps on several platforms, including iOS and JavaScript phones, Sonos systems and Roku, a brand that derived its name from the Japanese word for \"six\".\n\nPassages:\n\n[Roku]\nThe name comes from the Japanese word 六 (roku ) meaning \"six\" and was named so because it was the sixth company that Anthony Wood (CEO 2002-) started.\n\n[Rdio]\nRdio was an online music streaming service that offered ad-supported free streaming and ad-free subscription streaming services in 85 countries. It was available as a website and via app for Android, BlackBerry, iOS, and Windows Phone mobile devices, which could stream music from Rdio's servers or download music for offline playback; there were also clients for the Roku and Sonos systems.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qcfdeb546b2",
  "kind": "yes/no",
  "text": "Claim: The creator of The Life & Times of Tim and this man are not both art dealers. The other man currently owns the Nathaniel L. McCready House.\n\nPassages:\n\n[Nathaniel L. McCready House]\nIn 2011, the home was purchased by Larry Gagosian, who demolished the mansion's interior.\n\n[The Life &amp; Times of Tim]\nThe series was created by Steve Dildarian, and is about a hapless man in his mid-20s named Tim (voiced by Dildarian) who lives in New York City with his girlfriend Amy.\n\n[Steve Dildarian]\nSteve Dildarian (born November 3, 1969) is an American former advertising copywriter who is the creator, writer, producer and voice of Tim in the HBO animated television series \"The Life & Times of Tim\" (2008-2012).\n\n[Larry Gagosian]\nLawrence Gilbert \"Larry\" Gagosian (born April 19, 1945) is an Armenian American art dealer who owns the Gagosian Gallery chain of art galleries.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q97eb76736e",
  "kind": "yes/no",
  "text": "Claim: This airport is nearer to its local town than the airport near Interstate 687. The Truax Field Air National Guard Base is also located at that airport.\n\nPassages:\n\n[Dane County Regional Airport]\nDane County Regional Airport (DCRA) (IATA: MSN, ICAO: KMSN, FAA LID: MSN) (Truax Field) is a civil-military airport located six miles northeast of downtown Madison, the capital of Wisconsin.\n\n[Truax Field Air National Guard Base]\nTruax Field Air National Guard Base (IATA: MSN, ICAO: KMSN, FAA LID: MSN) , also known as Truax Field, is a military facility located at Dane County Regional Airport.\n\n[Interstate 687]\nThe highway would have connected I-90 in Albany to I-87 near Albany International Airport in Colonie.\n\n[Albany International Airport]\nAlbany International Airport (IATA: ALB, ICAO: KALB, FAA LID: ALB) is a public airport seven miles (11 km) northwest of Albany, in Albany County, New York, United States.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qca1fb3d695",
  "kind": "yes/no",
  "text": "Claim: Alberto Zaccheroni was the football coach who left for Milan the same year that the first golden goal scorer was topscorer for Udinese Calcio.\n\nPassages:\n\n[1998–99 Udinese Calcio season]\nWith topscorer Oliver Bierhoff, midfielder Thomas Helveg and coach Alberto Zaccheroni all departing for Milan, Udinese was looking to be on the back foot prior to the start of the season.\n\n[Oliver Bierhoff]\nOliver Bierhoff (] ; born 1 May 1968) is a retired German former footballer who scored the first golden goal in the history of major international football, for Germany in the Euro 96 final, a career-defining performance that vaulted him into the international limelight.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q4f4e0d4417",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Got very excited that my national trust card arrived I am officially a grandma https://t.co/mtkWJCxwom",
   "I am officially a national trust member"
  ]
 },
 {
  "qid": "q681a3adb3c",
  "kind": "yes/no",
  "text": "Claim: A wrestling group member that was born on March 1, 1987 in New England was Kyle O'Reilly. This wrestling group once won the ROH Tag Wars Tournament.\n\nPassages:\n\n[ReDRagon]\nreDRagon is a professional wrestling tag team consisting of Bobby Fish and Kyle O'Reilly.\n\n[Kyle O'Reilly]\nKyle Greenwood (born March 1, 1987) is a Canadian professional wrestler better known by the ring name Kyle O'Reilly, he is currently signed to WWE, where he performs in its developmental branch NXT.\n\n[ROH Tag Wars Tournament]\nTag Wars (formerly Trios Tournament) is a professional wrestling event held by Ring of Honor as a one-night tournament in 2005, 2006, 2010 and 2014 with the winners being Jimmy Rave, Alex Shelley and Abyss, The Kings of Wrestling and ReDRagon respectively.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q738a1fc876",
  "kind": "yes/no",
  "text": "Claim: Smriti Malhotra is the northern Indian politician that hosted a Hindi language Indian television talk show.\n\nPassages:\n\n[Smriti Irani]\nSmriti Zubin Irani (born Smriti Malhotra; 23 March 1976) is an Indian politician, former model, television actress and producer.\n\n[Kuch... Diiil Se]\nKuch... Diiil Se is a Hindi language Indian television talk show series hosted by Smriti Irani, which premiered on SAB TV on June 23, 2003.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q11c696fa45",
  "kind": "yes/no",
  "text": "Claim: The platform, for which the fixed shooter Proof of Destruction was developed, and Prológica CP-400 were not from the same country.\n\nPassages:\n\n[Commodore 16]\nThe Commodore 16 is a home computer made by Commodore International with a 6502-compatible 7501 or 8501 CPU, released in 1984 and intended to be an entry-level computer to replace the VIC-20. A cost-reduced version, the Commodore 116, was sold only in Europe.\n\n[Proof of Destruction]\nProof of Destruction (P.O.D.) is a 1987 fixed shooter for the Commodore 64 and Commodore 16 written by Shaun Southern and published by Mastertronic.\n\n[Prológica CP-400]\nIn the middle of 1984 a Brazilian company called Prológica, which made its own versions of 8 bits US computers, brought to the Brazilian market a new equipment for its personal computer series called \"CP\" (shorten of Personal Computer in Portuguese).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q9ec06d0543",
  "kind": "yes/no",
  "text": "Claim: An American rock band released My Animal. This band has more studio albums than the English band whose second album is Rispah.\n\nPassages:\n\n[The Invisible (band)]\nTheir self-titled debut album, released on 9 March 2009, was nominated for the Mercury Prize and selected as critics choice for iTunes album of the year.\n\n[Rispah]\nRispah is the second album by the English band The Invisible.\n\n[Boy Hits Car]\nBoy Hits Car released their 5th studio album \"All That Led Us Here\" in May 2014 and are following it up with a European tour.\n\n[My Animal]\nMy Animal (1998) is the debut album by American rock band Boy Hits Car.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qf66ef170e3",
  "kind": "yes/no",
  "text": "Claim: Danyang, Jiangusu and this city are both cities in China. This city was the birthplace of saxophonist Chen Xiuke.\n\nPassages:\n\n[Chen Xiuke]\nChen Xiuke (born 31 December 1976 in Dongfang, Hainan) is a male Chinese sports sailor.\n\n[Danyang, Jiangsu]\nDanyang () is a county-level city under the administration of Zhenjiang, Jiangsu province, China.\n\n[Dongfang, Hainan]\nDōngfāng () is one of the seven county-level cities of Hainan province, China.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qd29c4492e7",
  "kind": "yes/no",
  "text": "Claim: The song \"Only a Pawn in Their Game\" was based on a crime whose perpetrator was convicted in the year 1994.\n\nPassages:\n\n[Only a Pawn in Their Game]\n\"Only a Pawn in Their Game\" is a song written by Bob Dylan about the assassination of civil rights activist Medgar Evers.\n\n[Byron De La Beckwith]\nByron De La Beckwith, Sr. (November 9, 1920 – January 21, 2001) was an American white supremacist and Klansman from Greenwood, Mississippi, who in 1994 was convicted of assassinating civil rights leader Medgar Wiley Evers on June 12, 1963.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q7f366a5143",
  "kind": "yes/no",
  "text": "Claim: Johnnie Casson never appeared on ex-professional footballer Des O'Connor's British television show.\n\nPassages:\n\n[Johnnie Casson]\nJohnnie Casson is an English comedian who has appeared on numerous occasions on British television, notably on ITV's \"The Comedians\" and many guest spots on \"Des O'Connor Tonight\".\n\n[Des O'Connor]\nHe was evacuated to Northampton during the Second World War and was briefly a professional footballer with Northampton Town.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q3813321098",
  "kind": "yes/no",
  "text": "Claim: Chase Masterson made a cover of \"Burned With Desire\" that was never released for a 2008 neo-noir film. Paul Verhoeven is older than the director of that film.\n\nPassages:\n\n[Paul Verhoeven]\nPaul Verhoeven (] ; born 18 July 1938) is a Dutch film director, film producer, television director, television producer, and screenwriter.\n\n[James Kerwin]\nJames Kerwin (born October 13, 1973 in St. Louis, Missouri) is an American film and theatre director.\n\n[Yesterday Was a Lie]\nYesterday Was a Lie is a 2008 neo-noir film written and directed by James Kerwin and starring Kipleigh Brown, Chase Masterson, John Newton, and Mik Scriba.\n\n[Burned with Desire]\nA cover of the song was performed by Chase Masterson for an early cut of the motion picture \"Yesterday Was a Lie\", but not included in the commercial release of the film.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q05e9231fc2",
  "kind": "yes/no",
  "text": "Claim: Operation Diadem came before the conflict where Dave Schreiner was mortally wounded.\n\nPassages:\n\n[Dave Schreiner]\nHe was mortally wounded in action as a Marine on June 20, 1945 during the Battle of Okinawa and died the next day.\n\n[Operation Diadem]\nOperation Diadem, also referred to as the Fourth Battle of Monte Cassino or, in Canada, the Battle of the Liri Valley, was an offensive operation undertaken by the Allies of World War II (U.S. Fifth Army and British Eighth Army in May 1944, as part of the Italian Campaign of World War II.\n\n[Battle of Okinawa]\nThe Battle of Okinawa (Japanese: 沖縄戦 , Hepburn: Okinawa-sen ) (Okinawan: 沖縄戦 , \"Uchinaa ikusa \" ), codenamed Operation Iceberg, was a major battle of the Pacific War fought on the island of Okinawa by United States Marine and Army forces against the Imperial Japanese Army and included the largest amphibious assault in the Pacific War during World War II, the April 1, 1945, invasion of Okinawa itself.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q00d2ffbd1a",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Don’t keep up with the Jones’s",
   "Don’t keep up with the Joneses, the Joneses are broke!"
  ]
 },
 {
  "qid": "qb36fcd5fd0",
  "kind": "yes/no",
  "text": "Tweet: is this an earthquake because i am shook right now",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q4bbf81f868",
  "kind": "yes/no",
  "text": "Claim: The team that chose Joakim Noah for the 2007 NBA draft had a basketball player that Pekka Markkanen is the father of. That player whose father was Markkanen was traded for player Jimmy Butler III. Butler was born in Bhubaneswar.\n\nPassages:\n\n[Lauri Markkanen]\nIn the 2017 NBA draft, he was taken by the Minnesota Timberwolves with the 7th overall pick before being included in a trade to the Chicago Bulls for Jimmy Butler.\n\n[Joakim Noah]\nThe Chicago Bulls selected Noah with the ninth overall pick in the 2007 NBA draft.\n\n[Jimmy Butler (basketball)]\nJimmy Butler III (born September 14, 1989) is an American professional basketball player for the Minnesota Timberwolves of the National Basketball Association (NBA). Born in Houston, Butler grew up in Tomball, Texas, and played college basketball for Tyler Junior College and Marquette University.\n\n[Pekka Markkanen]\nMarkkanen is the father of Chicago Bulls basketball player Lauri Markkanen and the AIK football player Eero Markkanen.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q35b7ef5e82",
  "kind": "yes/no",
  "text": "Claim: The person who deposed Bernard Coard formed a military government with himself as chairman to rule Grenada, after the killing of a Grenadian politician who was the leader of the New Jewel Movement that was an effort in the areas of socio-economic development, education, and black liberation.\n\nPassages:\n\n[Bernard Coard]\nCoard launched a coup within the revolutionary government and took power for three days until he was himself deposed by General Hudson Austin.\n\n[Hudson Austin]\nAfter the killing of Maurice Bishop, he formed a military government with himself as chairman to rule Grenada.\n\n[Maurice Bishop]\nMaurice Rupert Bishop (29 May 1944 – 19 October 1983) was a Grenadian politician and the leader of New Jewel Movement – popular efforts in the areas of socio-economic development, education, and Black liberation – that came to power during the 13 March 1979 revolution that removed Eric Gairy from office.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 }
]
