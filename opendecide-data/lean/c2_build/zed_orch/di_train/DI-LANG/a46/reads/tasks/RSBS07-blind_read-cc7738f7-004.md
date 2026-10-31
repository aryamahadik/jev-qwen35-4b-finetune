# A46 replay label-noise blind read RSBS07-blind_read-cc7738f7-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS07-blind_read-cc7738f7-004.json

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
  "qid": "qc66a0c8387",
  "kind": "yes/no",
  "text": "Post: too many dudes are wearing birks with socks on. grow up. get the fucking toes out man.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qb7c4f732a3",
  "kind": "yes/no",
  "text": "Claim: Run-D.M.C. is the hip hop group from Hollis, Queens, New York, founded in 1981 by music producer Joseph Simmons, Darryl McDaniels, and Jason Mizell, that was brought out by the first rap crew from Dallas, Texas.\n\nPassages:\n\n[Run-DMC]\nRun-D.M.C. was an American hip hop group from Hollis, Queens, New York, founded in 1981 by Joseph Simmons, Darryl McDaniels, and Jason Mizell. Run-D.M.C. Run-D.M.C. Run-D.M.C. Run-D.M.C.\n\n[Nemesis (rap crew)]\nNemesis is the first rap crew from Dallas, Texas to enjoy popularity in the US and world-wide, thanks to their label, Profile Records, which was well known for bringing out many popular east coast rap releases such as Run-DMC, Dr. Jeckyll & Mr. Hyde, and Dana Dane.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qfe6ab31f97",
  "kind": "yes/no",
  "text": "Claim: This military leader led the military coup to remove Carlos Prío Socarrás from office. The Greek President served as inspiration for the composer of the song Quizás, Quizás, Quizás.\n\nPassages:\n\n[Carlos Prío Socarrás]\nCarlos Prío Socarrás (July 14, 1903 – April 5, 1977) was the President of Cuba from 1948 until he was deposed by a military coup led by Fulgencio Batista on March 10, 1952, three months before new elections were to be held.\n\n[Quizás, Quizás, Quizás]\nFarrés also received much help and inspiration for his lyrics from Cuban First Lady, Mary Tarrero-Serrano.\n\n[Fulgencio Batista]\nFulgencio Batista y Zaldívar (] ; born Rubén Zaldívar; January 16, 1901 – August 6, 1973) was the elected President of Cuba from 1940 to 1944, and U.S.-backed dictator from 1952 to 1959, before being overthrown during the Cuban Revolution.\n\n[Mary Tarrero-Serrano]\nShe was the second wife of Cuban President, Carlos Prio, who was overthrown by Fulgencio Batista in a military coup.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q71dca2ddbe",
  "kind": "yes/no",
  "text": "Claim: The three best sellers from the author of Detective (novel) that were released before Donna Tartt was born are \"Hotel\"and \"Airport\", from the 1960's, and \"Wheels\" from the 1970's.\n\nPassages:\n\n[Arthur Hailey]\nHis meticulously-researched books, which include such best sellers as \"Hotel\" (1965), \"Airport\" (1968), \"Wheels\" (1971), \"The Moneychangers\" (1975), and \"Overload\" (1979), have sold 170 million copies in 38 languages.\n\n[Detective (novel)]\nDetective is a novel by Arthur Hailey.\n\n[Donna Tartt]\nDonna Tartt (born December 23, 1963) is an American writer, the author of the novels \"The Secret History\" (1992), \"The Little Friend\" (2002), and \"The Goldfinch\" (2013).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qf2079e21f6",
  "kind": "yes/no",
  "text": "Claim: Esme Melville, was an Australian theatre and concert hall, television and film actress, she was nominated for Best Supporting Actress for her role of Miss Collard in \"Romulus, My Father\", an Australian drama film, directed by Richard Roxburgh, released in the year 2007.\n\nPassages:\n\n[Romulus, My Father (film)]\nRomulus, My Father is a 2007 Australian drama film directed by Richard Roxburgh.\n\n[Esme Melville]\nAt the 2007 Australian Film Institute Awards she was nominated for Best Supporting Actress for her role of Miss Collard in \"Romulus, My Father\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qd23335054b",
  "kind": "yes/no",
  "text": "Claim: The first major improved highway is located in Wheeling, West Virginia.\n\nPassages:\n\n[Mount Echo, West Virginia]\nMount Echo is an unincorporated community in Ohio County, West Virginia, United States. It is part of the Wheeling, West Virginia Metropolitan Statistical Area.\n\n[National Road]\nThe National Road (also known as the Cumberland Road) was the first major improved highway in the United States built by the federal government.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qfda1d252fb",
  "kind": "yes/no",
  "text": "Claim: Excalibur Hotel and Casino developed by William G. Bennett is the casino in Las Vegas now operated by MGM Resorts International.\n\nPassages:\n\n[Excalibur Hotel and Casino]\nExcalibur Hotel and Casino is a hotel and casino located on the Las Vegas Strip in Paradise, Nevada, in the United States. It is owned and operated by MGM Resorts International.\n\n[William G. Bennett (gaming executive)]\nUnder his leadership Circus Circus would go on to develop numerous additional properties throughout Nevada, including the Excalibur and Luxor casinos in Las Vegas.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qcedb217fbd",
  "kind": "yes/no",
  "text": "Claim: The Dumb and Dumber Movie is in the gross-out humour genre.\n\nPassages:\n\n[Dumb and Dumber To]\nDumb and Dumber To is a 2014 American comedy film co-written and directed by Bobby and Peter Farrelly.\n\n[Peter Farrelly]\nThe Farrelly brothers are mostly famous for directing and producing gross-out humor romantic comedy films such as \"Dumb and Dumber\", \"Shallow Hal\", \"Me, Myself and Irene\", \"There's Something About Mary\" and the 2007 remake of \"The Heartbreak Kid\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q68feceed22",
  "kind": "yes/no",
  "text": "Claim: A reggae artist is a believer in a religion that Roots reggae deals with the spiritual side of and was developed in Benin. A Time & Place is the second studio album by this artist.\n\nPassages:\n\n[Rastafari]\nClassified as a new religious movement, it developed in Jamaica during the 1930s.\n\n[Roots reggae]\nRoots reggae is a subgenre of reggae that deals with the everyday lives and aspirations of the artists concerned, including the spiritual side of Rastafari and the honoring of God, called Jah by Rastafari.\n\n[A Time &amp; Place]\nA Time & Place is the second studio album by reggae artist Julian Marley, released in 2003 on Lightyear Entertainment.\n\n[Julian Marley]\nHe follows into his father’s footsteps and is a devout Rastafarian who uses his music to inspire his life and spirituality.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q412ddfbd17",
  "kind": "yes/no",
  "text": "Claim: John Wayne Airport is further west than Muskegon County Airport.\n\nPassages:\n\n[John Wayne Airport]\nJohn Wayne Airport (IATA: SNA, ICAO: KSNA, FAA LID: SNA) is an international airport in Orange County, California, United States, with its mailing address in the city of Santa Ana, hence the IATA airport code.\n\n[Muskegon County Airport]\nMuskegon County Airport (IATA: MKG, ICAO: KMKG, FAA LID: MKG) is a county owned, public use airport in Muskegon County, Michigan, United States.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa78c6e6ab3",
  "kind": "yes/no",
  "text": "Claim: The white supremacist who wrote a biography about serial killer Joseph Paul Franklin founded the National Alliance major white nationalist organization.\n\nPassages:\n\n[Joseph Paul Franklin]\nJoseph Paul Franklin (born James Clayton Vaughn, Jr.; April 13, 1950 – November 20, 2013) was an American serial killer who gained notoriety for numerous murders in the late 1970s and early 1980s. His killing spree was the subject of a fictional novel entitled \"Hunter\" by White supremacist William L. Pierce, who said of Franklin that “he saw his duty as a white man and did what a responsible son of his race must do.”\n\n[William Luther Pierce]\nPierce founded the National Alliance, a major white nationalist organization, which he led for almost thirty years.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q70a9aa3cf8",
  "kind": "yes/no",
  "text": "Post: Is only 12 hours away from my first #raceforlife in memory of my grandma - Margaret Jackson who sadly passed away from cancer",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qb1e2841e07",
  "kind": "yes/no",
  "text": "Claim: Domenico Salvatori is a famous male singer with a voice equivalent to that of a soprano, mezzo-soprano, or contralto.\n\nPassages:\n\n[Domenico Salvatori]\nDomenico Salvatori (27 September 1855 – 11 December 1909) along with Alessandro Moreschi, Domenico Mustafà and Giovanni Cesari, was one of the famous castrati singers of the late 19th century.\n\n[Castrato]\nA castrato (Italian, plural: \"castrati\") is a type of classical male singing voice equivalent to that of a soprano, mezzo-soprano, or contralto.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q42599cb2bf",
  "kind": "yes/no",
  "text": "Claim: Legoman's Great Escape is a short film by Mike Sidorov and Michael Soare about a Legoman whose mission is to escape the G.I. Joe infested house while desperately trying to stay alive, G.I. Joe is a line of action figures produced and owned by the Hasbro toy company.\n\nPassages:\n\n[Legoman's Great Escape]\nLegoman's Great Escape is a short film by Mike Sidorov and Michael Soare about a Legoman whose mission is to escape the G.I. Joe infested house while desperately trying to stay alive.\n\n[G.I. Joe]\nG.I. Joe is a line of action figures produced and owned by the toy company Hasbro.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q97bbbcd5e3",
  "kind": "yes/no",
  "text": "Claim: The Czech player who was defeated by Johan Kriek in the 1982 Australian Open – Men's Singles and Albert Costa are both tennis players, and one of them, Costa, began playing at the age of five.\n\nPassages:\n\n[Albert Costa]\nCosta began playing tennis at the age of five.\n\n[Steve Denton]\nSteve Denton (born September 5, 1956, in Kingsville, Texas) is a former professional tennis player for the ATP Tour.\n\n[1982 Australian Open – Men's Singles]\nJohan Kriek was the defending champion, and successfully defended his title, defeating Steve Denton 6–3, 6–3, 6–2 in the final to win the Men's Singles title at the 1982 Australian Open, what was the rematch of the previous year.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe169cb4b94",
  "kind": "yes/no",
  "text": "Post: Everybody always talks about Devon Bostick’s portrayal of Rodrick in the Diary of a Wimpy Kid movies but nobody ever talks about how Devon Bostick played two separate characters in the Saw franchise",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qc16be6fb19",
  "kind": "yes/no",
  "text": "Claim: The venue in Orlando opened in 1936 and is found west of the home venue for the Orlando City SC. The 2017 Pro Bowl was played there.\n\nPassages:\n\n[Orlando City Stadium]\nIt is the home venue for the Orlando City SC, which entered Major League Soccer (MLS) as an expansion franchise in 2015, and their National Women's Soccer League (NWSL) sister club, the Orlando Pride.\n\n[2017 Pro Bowl]\nThe 2017 Pro Bowl (branded as the 2017 Pro Bowl presented by Aquafina for sponsorship reasons) was the National Football League's all-star game for the 2016 season which was played at Camping World Stadium in Orlando, Florida on January 29, 2017.\n\n[Camping World Stadium]\nCamping World Stadium, also known as the Orlando Citrus Bowl, is a stadium located in Orlando, Florida. The stadium is located in the West Lakes neighborhoods of Downtown Orlando, west of new sports and entertainment facilities including the Amway Center, the Dr. Phillips Center for the Performing Arts and the Orlando City Stadium.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q764b920fed",
  "kind": "yes/no",
  "text": "Claim: The friend of Russians Jean Follain and Connie May Fowler were not both memoirists.\n\nPassages:\n\n[Max Jacob]\nMax Jacob (] ; 12 July 1876 – 5 March 1944) was a French poet, painter, writer, and critic.\n\n[Jean Follain]\nFollain was a friend of Max Jacob, André Salmon, Jean Paulhan, Pierre Pussy, Armen Lubin, and Pierre Reverdy.\n\n[Connie May Fowler]\nConnie May Fowler (born January 3, 1960 to parents of multi-cultural backgrounds) is an American novelist, essayist, memoirist, screenwriter, and poet.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qe884f98fb4",
  "kind": "yes/no",
  "text": "Post: The best possible Saturday night is going out for dinner and drinks, having a couple too many, and being home for Match of the Day, happy weekend everyone",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q42890a7a4d",
  "kind": "yes/no",
  "text": "Claim: Siegi Sessler was the restaurateur whose club was frequented by Ruth Elizabeth \"Bette\" Davis an actress with Welsh ancestry.\n\nPassages:\n\n[Siegi Sessler]\nIt was well known to be the 'home away from home' for Hollywood stars, such as Frank Sinatra, Humphrey Bogart, Bob Hope, Crosby, Niven, Brando, Monroe, John Wayne, Cary Grant, Bette Davis, Clark Gable, Doris Day, Joan Crawford, Ingrid Bergman and Elizabeth Taylor.\n\n[Bette Davis]\nRuth Elizabeth \"Bette\" Davis (April 5, 1908 – October 6, 1989) was an American actress with Welsh ancestry of film, television, and theater.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q017592a795",
  "kind": "yes/no",
  "text": "Text: if i saw a capybara in person id probably throw up",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q1306eca6da",
  "kind": "yes/no",
  "text": "Tweet: I reverse imaged searched a selfie and it under visually similar images it is exclusively asian woman my am I white passing narrative is quaking",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q5fe0c72e59",
  "kind": "yes/no",
  "text": "Claim: Filmmakers Enrico Cocozza and Mira Nair have both been nominated for awards for their work.\n\nPassages:\n\n[Enrico Cocozza]\nEnrico Cocozza (6 November 1921 – 27 December 1997), was a Scottish filmmaker who won many film awards during the 1940s and 1950s.\n\n[Mira Nair]\n\", which was nominated for the Academy Award for Best Foreign Language Film.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q0f74925b45",
  "kind": "yes/no",
  "text": "Claim: Beatty Airport is a county-owned public-use airport located three nautical miles (6 km) southwest of the central business district of the unincorporated town of Beatty along the Amargosa River in Nye County, in the western U.S. state of Nevada.\n\nPassages:\n\n[Beatty Airport]\nBeatty Airport (IATA: BTY, ICAO: KBTY, FAA LID: BTY) is a county-owned public-use airport located three nautical miles (6 km) southwest of the central business district of Beatty, a town in Nye County, Nevada, United States.\n\n[Beatty, Nevada]\nBeatty (pronounced BAY-dee) is an unincorporated town along the Amargosa River in Nye County in the U.S. state of Nevada.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q35114a0ae9",
  "kind": "yes/no",
  "text": "Text: I just had to hide all ads from Crumbl cookies cause I’m fat and can’t resist temptation 😫",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q57b148be13",
  "kind": "yes/no",
  "text": "Claim: Avram Noam Chomsky, not the author of Memed, My Hawk, has writen more books.\n\nPassages:\n\n[Noam Chomsky]\nAvram Noam Chomsky ( ; born December 7, 1928) is an American linguist, philosopher, cognitive scientist, historian, social critic, and political activist. He is the author of over 100 books on topics such as linguistics, war, politics, and mass media.\n\n[Memed, My Hawk]\nMemed, My Hawk (Turkish: \"İnce Memed, meaning \"Memed, the Slim\"\" ) is a 1955 novel by Yaşar Kemal.\n\n[Yaşar Kemal]\nYaşar Kemal (born Kemal Sadık Gökçeli; 6 October 1923 – 28 February 2015) was a Turkish writer and human rights activist of Kurdish origin. He was one of Turkey's leading writers.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qcf19faebb5",
  "kind": "yes/no",
  "text": "Claim: The athlete, a qualifier for the June 2009 Manitoba Scotties Tournament of Hearts as reigning champion, was the captain of the gold medalist Curling team for Canada at the Sochi Winter Olympics.\n\nPassages:\n\n[2009 Manitoba Scotties Tournament of Hearts]\nThe reigning provincial champion, Jennifer Jones, won the 2008 Scotties Tournament of Hearts and thereby has already qualified for the 2009 event as Team Canada.\n\n[Jennifer Jones (curler)]\nShe won an Olympic gold medal as skip of the Canadian team at the 2014 Sochi Games. They won the 2008 World Women's Curling Championship, and were the last Canadian women's team to do so until Rachel Homan in 2017.\n\n[2007 Trail Appliances Autumn Gold Curling Classic]\nThe 2007 Trail Appliances Autumn Gold Curling Classic was the 30th annual edition of the event. It marked the first Grand Slam event of the Women's World Curling Tour. It was held October 5-9 at the Calgary Curling Club in Calgary, Alberta. The total purse for the event was $56,000 with $14,000 going to the winning team of Jennifer Jones, Cathy Overton-Clapham, Jill Officer and Dawn Askin.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8c8db693bf",
  "kind": "yes/no",
  "text": "Claim: A drummer was a member of \"The Nerves\" an Americana power pop trio. Americana musicians Blackie Lawless and this drummer were both born in 1956.\n\nPassages:\n\n[Blackie Lawless]\nBlackie Lawless (born Steven Edward Duren; September 4, 1956) is an American songwriter and musician best known as the lead singer and rhythm guitarist (formerly bassist) for the heavy metal band W.A.S.P.\n\n[Paul Collins (musician)]\nPaul Vincent Collins (born 1956, New York City) is an American writer, author, music producer, and multi-instrumentalist.\n\n[The Nerves]\nThe Nerves were a mid-1970s American power pop trio, based in Los Angeles, featuring guitarist Jack Lee, bassist Peter Case, and drummer Paul Collins.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qcea0dededa",
  "kind": "yes/no",
  "text": "Claim: Ana Beatriz Barros is a Brizilian actress and model known for appearances with an American designer of women's premium lingerie, the largest American retailer of women's lingerie, wholloy owned by L Brands.\n\nPassages:\n\n[Victoria's Secret]\nVictoria's Secret is an American designer, manufacturer, and marketer of women's premium lingerie, womenswear, and beauty products. Victoria's Secret is wholly owned by L Brands, a publicly traded company.\n\n[Ana Beatriz Barros]\nAna Beatriz Barros (born 29 May 1982) is a Brazilian model known for her multiple appearances in the \"Sports Illustrated Swimsuit Issue\" and for her work with Intimissimi, Guess? , bebe, Victoria's Secret, Chanel cosmetics, and Jennifer Lopez's JLO fashion line.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qe683125e53",
  "kind": "yes/no",
  "text": "Claim: One of the legendary four aces skaters was born in the third largest city in Norway. The others were Sten Stenson, Oscar Mathisen Award and Kay Stenshjemmet.\n\nPassages:\n\n[Trondheim]\nIt is the third largest city in the country, with a population (2013) of 169,972 inhabitants within the city borders.\n\n[Sten Stensen]\nTogether with Amund Sjøbrend, Kay Stenshjemmet, and Jan Egil Storholt, he was one of the legendary \"four S-es\" (\"four aces\" in Norwegian), contemporary Norwegian top skaters in the 1970s and early 1980s.\n\n[Jan Egil Storholt]\nJan Egil Storholt (born 13 February 1949) is a former speed skater from Norway. He was born in Trondheim.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qe67f641fe7",
  "kind": "yes/no",
  "text": "Claim: Nova Mob was the band formed by the man who released the interpretive dance piece '2541' after Hüsker Dü's breakup.\n\nPassages:\n\n[Grant Hart]\nGrant Vernon Hart (March 18, 1961 – September 13, 2017) was an American musician, best known as the drummer and co-songwriter for the alternative rock and hardcore punk band Hüsker Dü. After the band's breakup in 1988, he formed the alternative rock trio Nova Mob, where he moved to vocals and guitar.\n\n[2541]\n2541 is the first solo EP from Grant Hart, formerly of the band Hüsker Dü.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q2de7c22f6e",
  "kind": "yes/no",
  "text": "Tweet: Perfect way to end a 2+ hour @SunCountryAir deley: getting stuck on the tarmack at @mspairport waiting to go to a gate for almost an hour 🙄",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qadf8684e84",
  "kind": "yes/no",
  "text": "Text: ik the republicans r like tryna say they won but idk why they don’t just settle this w an instagram poll??",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q3e4be0e868",
  "kind": "yes/no",
  "text": "Claim: Dances with the Wolves star Wesley \"Wes\" Studi also had a role in a film featuring Amanda Wyss.\n\nPassages:\n\n[Wes Studi]\nWesley \"Wes\" Studi (Cherokee: ᏪᏌ ᏍᏚᏗ ) (born December 17, 1947) is a Cherokee actor and film producer from Nofire Hollow in Oklahoma. He has appeared in Academy Award-winning films, such as \"Dances with Wolves\" (1990) and \"The Last of the Mohicans\" (1992), and in the Academy Award-nominated films \"\" (1993) and \"The New World\" (2005).\n\n[Powwow Highway]\nWes Studi and Graham Greene, who were relatively unknown actors at the time, have small supporting roles.\n\n[Amanda Wyss]\nShe subsequently starred in \"Silverado\" (1985), \"Better Off Dead\" (1985), \"Powwow Highway\" (1989), \"Shakma\" (1990), and \"The Id\" (2016).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qd4a9b12129",
  "kind": "yes/no",
  "text": "Tweet: @c_j_mcburney Suspect there’s still room for you in the ground",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q33cb1c62ef",
  "kind": "yes/no",
  "text": "Claim: Genesee Cream Ale is a cold fermented, alcohlic beverage produced by a brewery located along the Genesee River.\n\nPassages:\n\n[Genesee Brewing Company]\nGenesee Brewing Company is an American brewery located along the Genesee River in Rochester, New York.\n\n[Genesee Cream Ale]\nGenesee Cream Ale is a cold fermented, alcohlic beverage produced by the Genesee Brewing Company in Rochester, NY.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qbd382950b1",
  "kind": "yes/no",
  "text": "Claim: Lance King has spent more time in the heavy metal music industry than Kevin DuBrow.\n\nPassages:\n\n[Kevin DuBrow]\nKevin Mark DuBrow (October 29, 1955 November 19, 2007) was an American heavy metal singer, best known as the lead vocalist of the heavy metal band Quiet Riot from 1975 until 1987, and again from 1990 until his death in 2007.\n\n[Lance King]\nLance King (born November 23, 1962) is an American heavy metal vocalist specializing in melodic rock progressive and power metal. Lance has sung with many groups over the last 35 years and started the record label Nightmare in 1990 to release his own music and is presently still at the helm of the label.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q88a036a445",
  "kind": "yes/no",
  "text": "Tweet: The fair-weather fans in all of these threads. Wake up call. Fleury is a human being. Surprise!",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qbb004df3a9",
  "kind": "yes/no",
  "text": "Claim: Nelson Pereira dos Santos is a director. So is the director of the movie Oscar Núñez played in, in 2000.\n\nPassages:\n\n[Nelson Pereira dos Santos]\nNelson Pereira dos Santos (born 22 October 1928) is a Brazilian film director.\n\n[Oscar Núñez]\nSome of his best known film credits included \"Nine Queens\" in 2000, \"Good Life Delivery\" in 2004, and \"Un novio para mi mujer\" in 2008.\n\n[Fabián Bielinsky]\nFabián Bielinsky (3 February 1959 – 28 June 2006) was an Argentine film director born in Buenos Aires.\n\n[Nine Queens]\nNine Queens (Spanish: Nueve Reinas ) is a 2000 Argentine crime drama film written and directed by Fabián Bielinsky and starring Ricardo Darín, Gastón Pauls, Leticia Brédice, Tomás Fonzi and Alejandro Awada.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc7a58db978",
  "kind": "yes/no",
  "text": "Claim: The Oppenheimer security hearing explored the associations of the wartime head of New Mexico laboratory.\n\nPassages:\n\n[Oppenheimer security hearing]\nThe Oppenheimer security hearing was a 1954 proceeding by the United States Atomic Energy Commission (AEC) that explored the background, actions, and associations of J. Robert Oppenheimer, the American scientist who had headed the Los Alamos Laboratory during World War II, where he played a key part in the Manhattan Project that developed the atomic bomb.\n\n[J. Robert Oppenheimer]\nOppenheimer was the wartime head of the Los Alamos Laboratory and is among those who are credited with being the \"father of the atomic bomb\" for their role in the Manhattan Project, the World War II undertaking that developed the first nuclear weapons used in the atomic bombings of Hiroshima and Nagasaki.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q804997dde6",
  "kind": "yes/no",
  "text": "Claim: Sir Thomas Daniel Courtenay was a supporting cast member of the film that Robert Emmet Smith art directed and was knighted in '01.\n\nPassages:\n\n[King Rat (film)]\nAmong the supporting cast were John Mills and Tom Courtenay.\n\n[Tom Courtenay]\nSir Thomas Daniel Courtenay ( ; born 25 February 1937) is an English actor who came to prominence in the early 1960s with a succession of films, including \"The Loneliness of the Long Distance Runner\" (1962), \"Billy Liar\" (1963), and \"Doctor Zhivago\" (1965). He received a knighthood in February 2001 for his service to cinema and theatre.\n\n[Robert Emmet Smith]\nHe was nominated for and Academy Award in the category Best Art Direction for the film \"King Rat\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qed3b0958d7",
  "kind": "yes/no",
  "text": "Claim: The A5117 runs between Shotwick and a village with a 2011 population of 4,972.\n\nPassages:\n\n[Helsby]\nHelsby is a village, civil parish and electoral ward in Cheshire, England, which in 2011 had a population of 4,972.\n\n[A5117 road]\nIt runs between Shotwick ( ) and Helsby ( ) and connects the A550 at Woodbank to the M56.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qe32872aa96",
  "kind": "yes/no",
  "text": "Claim: The producer of \"Coffin Rock\" worked on the film Wolf Creek which was loosely based on the murders of tourists by Ivan Milat in the 1990's.\n\nPassages:\n\n[Wolf Creek (film)]\nThe film was ambiguously marketed as being \"based on true events\"; the plot bore elements reminiscent of the real-life murders of tourists by Ivan Milat in the 1990s and Bradley Murdoch in 2001.\n\n[David Lightfoot]\nDavid Lightfoot worked on the horror films \"Wolf Creek\" and \"Rogue\".\n\n[Coffin Rock]\nCoffin Rock is an Australian melodramatic thriller film directed by Rupert Glasson and produced by David Lightfoot.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q1ac17f9c8a",
  "kind": "yes/no",
  "text": "Tweet: Using jazz as a reading playlist has reminded me one thing: I love Ella Fitzgerald",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q734b406477",
  "kind": "yes/no",
  "text": "Claim: Joseph Mansfield Santley was born first. The director of the movie that preceded Chow Yun-fat's City on Fire (1987 film) was born after him.\n\nPassages:\n\n[Joseph Santley]\nJoseph Mansfield Santley (born Joseph Ishmael Mansfield, January 10, 1890 – August 8, 1971) was an American actor, singer, dancer, writer, director, and producer of musical theatrical plays motion pictures and television shows.\n\n[John Woo]\nJohn Woo SBS (Ng Yu-Sum; born 1 May 1946) is a Chinese-born Hong Kong film director, writer, and producer.\n\n[City on Fire (1987 film)]\nFollowing \"A Better Tomorrow\" (1986), it helped establish Chow's popularity as an action star in Asia, and to a lesser degree, North America.\n\n[A Better Tomorrow]\nA Better Tomorrow () is a 1986 Hong Kong crime film directed by John Woo and starring Ti Lung, Leslie Cheung and Chow Yun-fat.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qa51f954e73",
  "kind": "yes/no",
  "text": "Claim: The university team with the fight song The Minnesota State Rouser has a mascot called Stomper. It began competing in the same conference as the St. Cloud State Huskies in 2008.\n\nPassages:\n\n[Stomper the Maverick]\nStomper the Maverick is the mascot for the Minnesota State Mavericks athletics teams of the Minnesota State University, Mankato and the associated club teams and charities.\n\n[Minnesota State Mavericks]\nMinnesota State began competition in the NSIC in 2008-09, due to the dissolution of the North Central Conference.\n\n[St. Cloud State Huskies]\nThe university is primarily a member of the Northern Sun Intercollegiate Conference (NSIC), and currently sponsors 18 NCAA Division II teams.\n\n[The Minnesota State Rouser]\nIt is played at all Minnesota State Mavericks athletics games, rallies and at many alumni events.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q8013810f54",
  "kind": "yes/no",
  "text": "Tweet: It’s spring, so that means it’s time for couples to leave the bar across the street and come fight under my window at 2 am again ❤️",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q013a3c3283",
  "kind": "yes/no",
  "text": "Claim: Dawn Roma French starred with Jennifer Julia Sawalha in both the movie that Al Pillay starred as \"Mary\" in and \"French and Julia Sawalha\".\n\nPassages:\n\n[Dawn French]\nDawn Roma French (born 11 October 1957) is an English actress, writer, and comedian. She is best known for starring in and writing for the comedy sketch show \"French and Saunders\" with comedy partner Jennifer Saunders and for playing the lead role as Geraldine Granger in the sitcom \"The Vicar of Dibley\".\n\n[Al Pillay]\nAlan \"Al\" Pillay also known as \"Al Pillay\" (born 22 August 1959), the star of \"Eat the Rich\" is a person of many names and two genders, starring in The Comic Strip Presents as Alan Pellay playing \"Himself\" in Gino (Episode 10) as Alana Pellay playing \"Herself\" in \"\" (Episode 13) and, finally, as Lana Pellay playing \"Mary\" in the feature movie, \"The Supergrass\".\n\n[The Supergrass]\nThe film starred Richardson, Adrian Edmondson, Jennifer Saunders, Dawn French, Keith Allen, Nigel Planer, Alexei Sayle, Ronald Allen and Robbie Coltrane.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2568a709d8",
  "kind": "yes/no",
  "text": "Claim: The apparent magnitude of the spiral galaxy discovered in 2015 by Frank Leavenworth is 15.18.\n\nPassages:\n\n[Francis Preserved Leavenworth]\nFrancis Preserved Leavenworth (born September 3, 1858 in Mount Vernon, Indiana; died November 12, 1928; a.k.a. \"Frank Leavenworth\") was an American astronomer.\n\n[NGC 166]\nNGC 166 (also known as PGC 2143) is a spiral galaxy located around 2.6 million light-years away in the constellation Cetus, with an apparent magnitude of 15.18.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc0e4ce762f",
  "kind": "yes/no",
  "text": "Claim: The band, who released \"My Type\", was a group of Elektra Records recording artists that are known to be an indie pop band.\n\nPassages:\n\n[My Type]\n\"My Type\" is a song by American indie pop band Saint Motel.\n\n[Saintmotelevision]\nIt was released on October 21, 2016, by Elektra Records.\n\n[Saint Motel]\nSaint Motel is an American indie pop band from Los Angeles, whose music has been described as everything from \"dream pop\" to \"indie prog\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 }
]
