# A46 replay label-noise blind read RSBS04-blind_read-f1becff1-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS04-blind_read-f1becff1-004.json

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
  "qid": "qb76edbe370",
  "kind": "yes/no",
  "text": "Claim: Newell Highway is the town located 10 km north of the Charcoal Tank Nature Reserve.\n\nPassages:\n\n[West Wyalong]\nWest Wyalong is a town in New South Wales, Australia, which is the main town of the Bland Shire, located in the Central West region of New South Wales. It is located on the crossroads of the Newell Highway between Melbourne and Brisbane, and the Mid-Western Highway between Sydney and Adelaide.\n\n[Charcoal Tank Nature Reserve]\nThe Charcoal Tank Nature Reserve is a protected nature reserve in the central western region of New South Wales, Australia. The 86.4 ha reserve is situated 10 km south of West Wyalong and may be accessed via the Newell Highway and The Charcoal Tank Road.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1cfd362057",
  "kind": "yes/no",
  "text": "Claim: Geographical Indication tag from Eastern Catholic government was given to the handicraft known for making simple loose clothing worn over the shoulders.\n\nPassages:\n\n[Shawl]\nA shawl (from Persian: lang-Urdu شال‎ ‎ \"shāl\", which may be from Hindi: दुशाला duśālā, ultimately from Sanskrit: शाटी śāṭī) is a simple item of clothing, loosely worn over the shoulders, upper body and arms, and sometimes also over the head.\n\n[Gopalpur Tussar Fabrics]\nThis handicraft received the Geographical Indication tag by the Government of India in 2009.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf74f3d6533",
  "kind": "yes/no",
  "text": "Claim: Olivia DeJonge starred in an American horror film directed by Shyamalan called The Visit.\n\nPassages:\n\n[Olivia DeJonge]\nOlivia DeJonge (born 30 April 1998) is an Australian actress, known for playing Tara Swift / Shaneen Quigg in the series \"Hiding\" and Becca in the film \"The Visit\".\n\n[The Visit (2015 American film)]\nThe Visit is a 2015 American found footage horror film written and directed by M. Night Shyamalan, and starring Olivia DeJonge, Ed Oxenbould, Deanna Dunagan, Peter McRobbie, and Kathryn Hahn.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3f423ea0c2",
  "kind": "yes/no",
  "text": "Claim: Clement Richard Attlee served as a Prime Minister in postwar Britain.\n\nPassages:\n\n[The Spirit of '45]\nThe Spirit of '45 is a 2013 documentary film by British director Ken Loach, focused on and celebrating the radical changes in postwar Britain under the Labour government of Clement Attlee, which came to power in 1945.\n\n[Clement Attlee]\nClement Richard Attlee, 1st Earl Attlee, {'1': \", '2': \", '3': \", '4': \"} (3 January 1883 – 8 October 1967) was a British Labour politician who served as Prime Minister of the United Kingdom from 1945 to 1951 and Leader of the Labour Party from 1935 to 1955.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qae58d7e877",
  "kind": "yes/no",
  "text": "Claim: Nobody Loves You was written by John Lennon and released on the album, Walls and Bridges, which was issued by Apple Records, and was written, recorded, and released during his 18 month separation from artist Yoko Ono.\n\nPassages:\n\n[Nobody Loves You (When You're Down and Out)]\n\"Nobody Loves You (When You're Down and Out)\" is a song written by John Lennon released on his 1974 album \"Walls and Bridges\".\n\n[Walls and Bridges]\nIt was issued by Apple Records on 26 September 1974 in the United States and on 4 October in the United Kingdom. Written, recorded and released during his 18-month separation from Yoko Ono, the album captured Lennon in the midst of his \"Lost Weekend\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc5407f13c3",
  "kind": "yes/no",
  "text": "Claim: HeroClix is a collectible miniatures game where players construct teams from various video games such as a fighting video game franchise developed and published by Capcom.\n\nPassages:\n\n[HeroClix]\nHeroClix is a collectible miniatures game that uses the Clix system that centers on the world of superhero comic books, especially the Marvel and DC Comics universes. Players construct teams of comic book heroes, villains, or characters from various video games series such as Street Fighter, Gears of War, and Halo and engage in a turn-by-turn battle on grid maps based on various storyline locations.\n\n[Street Fighter]\nStreet Fighter (ストリートファイター , Sutorīto Faitā ) , commonly abbreviated as \"SF\" or スト (\"Suto\"), is a fighting video game franchise developed and published by Capcom.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qdab8f538ea",
  "kind": "yes/no",
  "text": "Claim: Aurangabad, titled \"The City of Gates\", is the city that publishes the Marathi daily newspaper 'Loksatta'.\n\nPassages:\n\n[Loksatta]\n\"Loksatta\" is published out of Mumbai, Pune, Nagpur, Ahmednagar, Aurangabad, and Delhi.\n\n[Aurangabad, Maharashtra]\nThe administrative headquarters of the Aurangabad Division or Marathwada region, Aurangabad is titled \"The City of Gates\" and the strong presence of these can be felt as one drives through the city.The City was founded in 1610 by Malik Amber which in the year 2010 completed 400 years.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qe3001fdb28",
  "kind": "yes/no",
  "text": "Claim: The star of a TV show won Golden Globe Awards in 1996. An actor who appeared in this TV show also had a pivotal role in the 1997 film \"Inferno\".\n\nPassages:\n\n[Peter Boyle]\nBoyle, who won an Emmy Award in 1996 for a guest-starring role on the science-fiction drama \"The X-Files\", won praise in both comedic and dramatic parts following his breakthrough performance in the 1970 film \"Joe\".\n\n[Michael Cavanaugh (actor)]\nHis television guest-credits include \"The West Wing\", \"Joe Bash\", \"Starman\", \"Hunter\", \"Monk\" and \"24\".\n\n[Joe Bash]\nStarring Peter Boyle as a weary and embittered New York City Police Department beat cop, it was created by veteran TV producer Danny Arnold following his successful New York City police detective sitcom \"Barney Miller\".\n\n[Inferno (1997 film)]\nEvan Lurie, Michael Cavanaugh and Tané McClure appear in other pivotal roles.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q9d87607569",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Thinking about that time Blizzard had the brilliant idea to change everyone's name on their forums to their real names. God, what an idea that was.",
   "\"The idea Blizzard had to stop people from being terrible on the internet was a bad one that would have led to people being doxxed at best, murdered at worst.\""
  ]
 },
 {
  "qid": "q36efef8c8f",
  "kind": "yes/no",
  "text": "Text: Maybe if we didn’t comment on things that don’t concern us, the world would be a happier place?? But what do I know🤷🏻‍♀️",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qa75f318a47",
  "kind": "yes/no",
  "text": "Claim: Jean Terrell replaced Diana Ross as the lead singer of The Supremes in 1969 and provided the lead vocals on the song \"You Gotta Have Love in Your Heart\" by the Supremes and the Four Tops.\n\nPassages:\n\n[Jean Terrell]\nShe replaced Diana Ross as the lead singer of The Supremes in January 1970.\n\n[You Gotta Have Love in Your Heart]\n\"You Gotta Have Love in Your Heart\" is a duet single between Motown singing groups The Supremes and the Four Tops, released as a single from their \"The Return of the Magnificent 7\" album in 1971. Lead vocals were by the groups' respective lead singers Jean Terrell and Levi Stubbs.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf84ba6aa34",
  "kind": "yes/no",
  "text": "Text: how close i am to losing it. https://t.co/iQ5onEyYhb",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qc28ece1166",
  "kind": "yes/no",
  "text": "Claim: Chad Smith and another artist are American. This other singer released the song \"Stone Cold Gentleman\".\n\nPassages:\n\n[Stone Cold Gentleman]\n\"Stone Cold Gentleman\" is a song performed by American contemporary R&B singer Ralph Tresvant, issued as the second single from his eponymous debut album.\n\n[Chad Smith]\nChadwick Gaylord Smith (born October 25, 1961) is an American musician and the current drummer of the Red Hot Chili Peppers, which he joined in 1988.\n\n[Ralph Tresvant]\nRalph Edward Tresvant Sr. (born May 16, 1968), also known as Rizz and Rizzo, is an American contemporary R&B singer best known as the lead singer of R&B/pop group New Edition.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q6fefbdcf2e",
  "kind": "yes/no",
  "text": "Claim: The man that composed the opera Irrelohe was also a teacher. The composer, who American Violinist Tim Fain is best known for working with, was not.\n\nPassages:\n\n[Philip Glass]\nPhilip Morris Glass (born January 31, 1937) is an American composer.\n\n[Irrelohe]\nIrrelohe is an opera in three acts by the Austrian composer Franz Schreker, libretto by the composer.\n\n[Tim Fain]\nTim Fain is an American violinist, perhaps best known for his performances in the movie \"Black Swan\" and his work with American composer Philip Glass.\n\n[Franz Schreker]\nFranz Schreker (originally \"Schrecker\"; 23 March 1878, Monaco – 21 March 1934, Berlin) was an Austrian composer, conductor, teacher and administrator.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc705302294",
  "kind": "yes/no",
  "text": "Claim: Greatest Hits Volume 1 is a greatest hits compilation album by The Beatles which was exclusive to Australia and New Zealand, the album was compiled by EMI Australia to fill in the gap, much like A Collection of Beatles Oldies (subtitled But Goldies!), by the English rock band the Beatles.\n\nPassages:\n\n[A Collection of Beatles Oldies]\nA Collection of Beatles Oldies (subtitled But Goldies!)\n\n[Greatest Hits Volume 1 (Beatles album)]\nThe album was compiled by EMI Australia to fill in the gap between \"Rubber Soul\" and \"Revolver\" (much like \"A Collection of Beatles Oldies\" would in 1966 in between \"Revolver\" and \"Sgt. Pepper's Lonely Hearts Club Band\").",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q4b0f0eaf9c",
  "kind": "yes/no",
  "text": "Claim: An assistant coach for Orlando Magic, Under doc rivers and the head coach of the 1997–98 Orlando Magic season led United States men's Olympic basketball team to the gold medal at the 1992 Summer Olympics. Yanni Hufnagel served under this coach.\n\nPassages:\n\n[Chuck Daly]\nCharles Jerome Daly (July 20, 1930 – May 9, 2009) was an American basketball head coach. He led the Detroit Pistons to consecutive National Basketball Association (NBA) Championships in 1989 and 1990, and the 1992 United States men's Olympic basketball team (\"The Dream Team\") to the gold medal at the 1992 Summer Olympics.\n\n[Eric Musselman]\nThe son of former NBA head coach Bill Musselman, Eric Musselman was a head coach in the Continental Basketball Association (CBA) before becoming an assistant coach with the Minnesota Timberwolves, Orlando Magic (under Chuck Daly and Doc Rivers), and Atlanta Hawks (under Lon Kruger).\n\n[Yanni Hufnagel]\nHe last served as an assistant coach of the Nevada Wolf Pack men's basketball team under Eric Musselman.\n\n[1997–98 Orlando Magic season]\nThe Magic hired Chuck Daly as head coach, who won two championships coaching the Detroit Pistons.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qbd2c2d0ee1",
  "kind": "yes/no",
  "text": "Claim: Lord of the Rings actor Elijah Wood starred alongside Paul Hogan in a movie that features actor-model Jessica Wesson is a supporting role.\n\nPassages:\n\n[Flipper (1996 film)]\nFlipper is a 1996 adventure film remake of the 1963 film of the same name (which in turn begat a TV series that ran from 1964 to 1967), starring Paul Hogan and Elijah Wood.\n\n[Elijah Wood]\nHe is best known for his high-profile leading role as Frodo Baggins in Peter Jackson's epic film trilogy \"The Lord of the Rings\" (2001–03).\n\n[Jessica Wesson]\nShe is best known for her recurring role as Jennifer Sudarsky, Brad's (Zachery Ty Bryan) first girlfriend on the sitcom \"Home Improvement\", and having supporting roles in the Universal films \"Casper\" and \"Flipper\" in the 1990s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qbedbcae4d5",
  "kind": "yes/no",
  "text": "Claim: American actor and comedian Dan Castellaneta voiced the cartoon character in the animated television series in which Pablo Aurrecochea wears kits adorned with its cartoon characters.\n\nPassages:\n\n[Pablo Aurrecochea]\nHe is usually known for wearing kits adorned with cartoon characters such as Tom and Jerry, Krusty the Clown, The Incredible Hulk, and others.\n\n[Krusty the Clown]\nHerschel Shmoikel Pinchas Yerucham Krustofsky, better known as Krusty the Clown (sometimes spelled as Krusty the Klown), is a cartoon character in the animated television series \"The Simpsons\". He is voiced by Dan Castellaneta.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qde4052f8b1",
  "kind": "yes/no",
  "text": "Claim: Lewis Moran was murdered a week after the death of the Italian hitman from the Australian city of Melbourne.\n\nPassages:\n\n[Andrew Veniamin]\nAndrew \"Benji\" Veniamin (16 November 1975 – 23 March 2004) was an Australian criminal from Melbourne, Victoria, Australia.\n\n[Lewis Moran]\nHis murder occurred one week after the funeral of fellow Melbourne underworld criminal and suspected hitman Andrew Veniamin.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa9657282f4",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "I hate that my professor isn't responding to me after I immediately replied to her email.",
   "i love when i respond to my professor immediately after she emailed me and i still haven’t gotten a response :)) (it’s been almost 4 hours) :))"
  ]
 },
 {
  "qid": "q7ce394b96d",
  "kind": "yes/no",
  "text": "Claim: David Michael Draiman was born before the vocalist of the song Make Me Smile.\n\nPassages:\n\n[Make Me Smile]\n\"Make Me Smile\" is a song written by James Pankow for the rock band Chicago with the band's guitarist, Terry Kath, on lead vocals.\n\n[David Draiman]\nDavid Michael Draiman (born March 13, 1973) is an American songwriter and the vocalist for the band Disturbed as well as for the band Device.\n\n[Terry Kath]\nTerry Alan Kath (January 31, 1946 – January 23, 1978) was an American musician and songwriter, best known as the original guitarist, one of the lead singers and founding members of the rock band Chicago.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qefa0a0b6b1",
  "kind": "yes/no",
  "text": "Claim: The 2011 Toledo Rockets football team was invited to an event where they defeated the Air Force 42–41. 22 matches have been played by the U.S. men's national soccer team in the stadium that hosted that event.\n\nPassages:\n\n[2011 Military Bowl]\nThe 2011 Military Bowl Presented by Northrop Grumman, the fourth edition of the game, was a post-season American college football bowl game, held on December 28, 2011 at Robert F. Kennedy Memorial Stadium in Washington, D.C. as part of the 2011–12 NCAA bowl season.\n\n[Robert F. Kennedy Memorial Stadium]\nThe U.S. men's national soccer team has played 22 matches there from 1977 to 2013, more than any other stadium.\n\n[2011 Toledo Rockets football team]\nThey were invited to the Military Bowl where they defeated Air Force 42–41.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qac5cb50f88",
  "kind": "yes/no",
  "text": "Claim: Caroline Cruice Goodall, is an English actress and screenwriter, her other film appearances include the October 2015 Australian revenge comedy-drama film, The Dressmaker, written and directed by Jocelyn Moorhouse, based on the novel of the same name by Rosalie Ham.\n\nPassages:\n\n[Caroline Goodall]\nHer other film appearances include \"Hook\" (1991), \"Cliffhanger\" (1993), \"Schindler's List\" (1993), \"Disclosure\" (1994), \"White Squall\" (1996), \"The Princess Diaries\" (2001) and \"The Dressmaker\" (2015).\n\n[The Dressmaker (2015 film)]\nThe Dressmaker is a 2015 Australian revenge comedy-drama film written and directed by Jocelyn Moorhouse, based on the novel of the same name by Rosalie Ham.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5363130d31",
  "kind": "yes/no",
  "text": "Claim: Judy Hample is a former chancellor of this educational organization. The organization and State University System of this state, for which Elwyn Thomas was a Supreme Court Justice from 1938 to 1969, have the United States in common.\n\nPassages:\n\n[Florida Board of Regents]\nThe Florida Board of Regents was from 1965 to 2001 the governing body for the State University System of Florida, which includes all public universities in the state of Florida, United States.\n\n[Elwyn Thomas]\nElwyn Thomas (July 5, 1894 – February 15, 1971) was a Florida judge, and a Justice of the Florida Supreme Court from 1938 to 1969.\n\n[State University System of Florida]\nThe State University System of Florida (SUS, or SUSF out-of-state) is a system of twelve public universities in the U.S. state of Florida.\n\n[Judy Hample]\nShe is the former chancellor of the Pennsylvania State System of Higher Education and the Florida Board of Regents.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qd0edb62e43",
  "kind": "yes/no",
  "text": "Claim: The host of the TV series that Fletcher Pilon is known for winning the eighth season of, was born in Orhei, Victoria\n\nPassages:\n\n[Fletcher Pilon]\nFletcher Pilon (born 6 April 2001) is an Australian acoustic singer and songwriter, known for winning the eighth season of \"Australia's Got Talent\" in March 2016.\n\n[Australia's Got Talent (season 8)]\nMorris did not return as host as she is committed to another show and was replaced by Dave Hughes as the host.\n\n[Dave Hughes]\nDavid William \"Hughesy\" Hughes (born 26 November 1970 in Warrnambool, Victoria) is an Australian stand-up comedian, and a radio and television presenter.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q037aa90198",
  "kind": "yes/no",
  "text": "Claim: Light quadricycles (L6e), and heavy quadricycles (L7e) are the two categories of the non-electric version of the neighbourhood electric bike.\n\nPassages:\n\n[Neighborhood Electric Vehicle]\nThe non-electric version of the neighbourhood electric vehicle is the Motorised quadricycle.\n\n[Motorised quadricycle]\nTwo categories are defined; knowingly light quadricycles (L6e), and heavy quadricycles (L7e).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q6e72eb2f60",
  "kind": "yes/no",
  "text": "Claim: Bruce Darnell was a jury member for a German talent show Vanessa Krasniqi took part in. He was also an American model and choreographer born in 1950's.\n\nPassages:\n\n[Vanessa Krasniqi]\nShe rose to fame after taking part in the ninth season of the German talent show \"Deutschland sucht den Superstar\".\n\n[Bruce Darnell]\nBruce Darnell (born July 19, 1957) is an American model and choreographer based in Germany.\n\n[Deutschland sucht den Superstar (season 9)]\nJury members Fernanda Brandao and Patrick Nuo left DSDS and were replaced by Bruce Darnell and Cascada's Natalie Horler.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qcc1789b845",
  "kind": "yes/no",
  "text": "Claim: The actress that starred in Cerberus (film) played a supporting role in an animated film.\n\nPassages:\n\n[40 Days and 40 Nights]\n40 Days and 40 Nights is a 2002 satirical erotic romantic comedy film directed by Michael Lehmann, written by Rob Perez and starring Josh Hartnett, Shannyn Sossamon and Paulo Costanzo.\n\n[Cerberus (film)]\nCerberus (also known as Cerberus: the Guardian of Hell), is a 2005 Sci Fi Channel original film, starring Sebastian Spence, Emmanuelle Vaugier, and Greg Evigan.\n\n[Emmanuelle Vaugier]\nShe appeared as Addison Corday in \"Saw\" \"II\" and \"IV\", and had a supporting role in the Josh Hartnett film \"40 Days and 40 Nights\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q23244971b9",
  "kind": "yes/no",
  "text": "Claim: Elena Kagan, skewered in \"Newsical\", is an Associate Justice of the Supreme Court of the United States.\n\nPassages:\n\n[Newsical]\nEveryone from President Barack Obama, Lady Gaga, Nancy Grace and Oprah Winfrey to Christina Aguilera, Elena Kagan, Dr.Phill and Sarah Palin are skewered.\n\n[Elena Kagan]\nElena Kagan (pronounced ; born April 28, 1960) is an Associate Justice of the Supreme Court of the United States.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q989105efc0",
  "kind": "yes/no",
  "text": "Claim: The film Christopher Robin has fewer writers than the 1984 film that Mermaid Got Married was based on.\n\nPassages:\n\n[Splash (film)]\nSplash is a 1984 American fantasy romantic comedy film directed by Ron Howard, written by Lowell Ganz and Babaloo Mandel, and starring Tom Hanks, Daryl Hannah, John Candy, and Eugene Levy.\n\n[Christopher Robin (film)]\nChristopher Robin is an upcoming American comedy-drama adventure film directed by Marc Forster, with a screenplay written by Tom McCarthy, Alex Ross Perry, and Allison Schroeder.\n\n[Mermaid Got Married]\nBased on the 1984 American film \"Splash\", the plot involves a mermaid who travels onto land and falls in love with a human man.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q59523b4478",
  "kind": "yes/no",
  "text": "Claim: Sunrise Avenue and the band, who released the album \"You Could Have It So Much Better \", were neither formed in 2002.\n\nPassages:\n\n[Franz Ferdinand (band)]\nFranz Ferdinand are a Scottish rock band, formed in 2002 and based in Glasgow.\n\n[You Could Have It So Much Better]\nYou Could Have It So Much Better is the second studio album by Scottish indie rock band Franz Ferdinand.\n\n[Sunrise Avenue]\nSunrise Avenue is a Finnish rock band originally formed in 2002 in Helsinki, Finland.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qcbafd63482",
  "kind": "yes/no",
  "text": "Claim: The head office of József Váradi's airline is located in Mountain View.\n\nPassages:\n\n[Wizz Air]\n\" ), is a Hungarian low-cost airline with its head office in Budapest.\n\n[József Váradi]\nJózsef Janos Váradi (born 21 September 1965) is a Hungarian businessman who co-founded Wizz Air and has been its CEO since 2003.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q6da7602fe6",
  "kind": "yes/no",
  "text": "Claim: The Professor of Law at the Interdisciplinary Center in Herzliya holds the position of the Supreme Court Judge.\n\nPassages:\n\n[Kahan Commission]\nIts other two members were Supreme Court Judge Aharon Barak, and Major general (res.)\n\n[Aharon Barak]\nAharon Barak (Hebrew: אהרן ברק‎ , born Aharon Brick, 16 September 1936) is a Professor of Law at the Interdisciplinary Center in Herzliya and a lecturer in law at the Hebrew University of Jerusalem, the Yale Law School, Central European University, Georgetown University Law Center, and the University of Toronto Faculty of Law.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q5e5ff21435",
  "kind": "yes/no",
  "text": "Text: I got asked if I needed a kid’s menu today...21 is treating me well 👶🏼",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q1cf2d8ef1e",
  "kind": "yes/no",
  "text": "Post: me and noah forgot that today is our anniversary. if that isn’t couple goals then idk what is 😌",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qe527a90c2d",
  "kind": "yes/no",
  "text": "Claim: The name of the pop band founded by one of the stars of country music group Aisa Yeh Jahaan is Euphoria.\n\nPassages:\n\n[Aisa Yeh Jahaan]\nThe film is India's first carbon neutral film and stars Palash Sen, Ira Dubey and Kymsleen Kholie in lead roles, with Yashpal Sharma, Saurabh Pandey, Tinu Anand, Carol Gracias, Prisha Dabbas and Saurabh Pandey in supporting roles.\n\n[Palash Sen]\nPalash Sen is an Indian singer, songwriter, musician, composer and actor best known as the founder and frontman of India's pop band Euphoria.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q336f51949e",
  "kind": "yes/no",
  "text": "Claim: Long relay is the other name for this athletics competition event in which Papa M'Baye N'Diaye competed at the 1964 Summer Olympics and the 1968 Summer Olympics.\n\nPassages:\n\n[Papa M'Baye N'Diaye]\nHe competed in the 4 × 400 metres relay at the 1964 Summer Olympics and the 1968 Summer Olympics.\n\n[4 × 400 metres relay]\nThe 4 × 400 metres relay or long relay is an athletics track event in which teams consist of four runners who each complete 400 metres or one lap.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa66f33a2a0",
  "kind": "yes/no",
  "text": "Claim: The band whose song \"Rattled by the Rush\" was the first single for its third album, \"Paul Stanley,\" went on a well-received reunion tour in the year 2010.\n\nPassages:\n\n[Rattled by la Rush]\n\"Rattled by the Rush\" is a single/EP released by indie rock group Pavement in 1995. It is recognized as the single for the song \"Rattled by the Rush\", the first single from the band's third album, \"Wowee Zowee\" (1995).\n\n[Pavement (band)]\nPavement was an American indie rock band that formed in Stockton, California in 1989. In 2010, they undertook a well-received reunion tour.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qdd10a716e2",
  "kind": "yes/no",
  "text": "Claim: James Nestor is a writer. He has written for a publication that was published after the publication responsible for the Global Open Access Forum.\n\nPassages:\n\n[Dwell (magazine)]\nIt was launched with a magazine in September 2000 to bridge the gap between design professionals and enthusiasts by Lara Hedberg Deam with architecture and design critic Karrie Jacobs as its Editor-in-Chief.\n\n[American Scientist]\nAmerican Scientist (informally abbreviated AmSci) is an American bimonthly science and technology magazine published since 1913 by Sigma Xi, The Scientific Research Society.\n\n[Global Open Access Forum]\nIt was created by the American Scientist, which is published by Sigma Xi, in September 1998, before the term \"Open Access\" (OA) was coined, and it was originally called the \"September98-Forum.\"\n\n[James Nestor (writer)]\nJames Nestor is a San Francisco-based journalist who has written for \"Outside magazine\", \"Men's Journal\", \"Dwell\" magazine, National Public Radio, \"The New York Times\", the San Francisco Chronicle magazine, and others.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q1f7e747270",
  "kind": "yes/no",
  "text": "Claim: At the 2011 census the population of the city where the athlete was born was 6,960. She won 2 medals for the country where Parap, Northern Territory is at the World Championship in Athletics.\n\nPassages:\n\n[Parap, Northern Territory]\nParap is an inner suburb of the city of Darwin, Northern Territory, Australia.\n\n[Australia at the World Championships in Athletics]\nCathy Freeman, Jana Pittman and Sally Pearson are Australia's only multiple gold medal winners, Freeman (bronze) and Pearson (silver) have also each won a place medal. . Other multiple medalists are: Dimitri Markov (1 gold, 1 silver), (2 golds), Jared Tallent (1 silver, 2 bronzes), Kerry Saxby-Junna (1 silver, 1 bronze) and Mitchell Watt (1 silver, 1 bronze).\n\n[Young, New South Wales]\nAt the 2011 census , Young had a population of 6,960.\n\n[Kerry Saxby-Junna]\nShe was born in Young, New South Wales and grew up in Ballina, New South Wales.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q15891d38a3",
  "kind": "yes/no",
  "text": "Claim: The child actor, who played the character Fenmore Baldwin, plays in a series that follows a group of friends who run an Irish bar in it's Always Sunny in Philadelphia.\n\nPassages:\n\n[It's Always Sunny in Philadelphia]\nThe series follows the exploits of \"The Gang\", a group of debauched self-centered friends who run the Irish bar Paddy's Pub in South Philadelphia.\n\n[Fenmore Baldwin]\nInitially portrayed by various child actors including Robbie Tucker, the character was rapidly aged to a teenager in 2012, with Max Ehrich assuming the role.\n\n[Robbie Tucker]\nRobbie Tucker (born April 5, 2001) is an American actor. Tucker has also starred on other series, such as \"Criminal Minds\", \"FlashForward\" and \"It's Always Sunny in Philadelphia\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q70f900ad09",
  "kind": "yes/no",
  "text": "Claim: The award given to Matt James in 2012 has its name derived from the EN World web site.\n\nPassages:\n\n[Matt James (game designer)]\nIn 2012 James won an ENnie Award for \"\" and has been nominated for several Origins Awards.\n\n[ENnies]\nThe name of the award is derived from the EN World web site that has hosted the awards since their inception in 2001.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc01696d086",
  "kind": "yes/no",
  "text": "Tweet: Good morning to everyone again, except Eddie Reynoso, his lab rats &amp; whoever the fuck is letting Oscar Valdez fight after failing a drugs test - just because it would be bad for business.\n\nSome things more important than money, but not in boxing - clearly.\n\n❌💉",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q81f113dd40",
  "kind": "yes/no",
  "text": "Claim: Los Angeles Historic-Cultural Monument (No. 139) hosted an event by the IFBB professional bodybuilding organization on Oct 12, 1991.\n\nPassages:\n\n[1991 Ms. Olympia]\nThe 1991 Ms. Olympia contest was an IFBB professional bodybuilding competition was held on October 12 and 13, 1991 at the Shrine Auditorium in Los Angeles, California.\n\n[Shrine Auditorium]\nIt was designated a Los Angeles Historic-Cultural Monument (No. 139) in 1975.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q1512080836",
  "kind": "yes/no",
  "text": "Claim: The leader of the Confederate Army of Tennessee during Hood's Tennessee Campaign died on August 30, 1879 in Hawaii.\n\nPassages:\n\n[John Bell Hood]\nJohn Bell Hood (June 1 or June 29, 1831 – August 30, 1879) was a Confederate general during the American Civil War. Arguably one of the best brigade and division commanders in the Confederate States Army, Hood gradually became increasingly ineffective as he was promoted to lead larger, independent commands late in the war; his career and reputation were marred by his decisive defeats leading an army in the Atlanta Campaign and the Franklin–Nashville Campaign.\n\n[Franklin–Nashville Campaign]\nThe Franklin–Nashville Campaign, also known as Hood's Tennessee Campaign, was a series of battles in the Western Theater, conducted from September 18 to December 27, 1864, in Alabama, Tennessee, and northwestern Georgia during the American Civil War. The Confederate Army of Tennessee under Lt. Gen. John Bell Hood drove north from Atlanta, threatening Maj. Gen. William T. Sherman's lines of communications and central Tennessee.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q15a23ccc04",
  "kind": "yes/no",
  "text": "Claim: South America is the region that does not have the indigenous language that includes the word which is the common name of a species of plant called \"Erythroxylum vacciniifolium \".\n\nPassages:\n\n[Erythroxylum]\nAnother species, \"Erythroxylum vacciniifolium\" (also known as Catuaba) is used as an aphrodisiac in Brazilian drinks and herbal medicine.\n\n[Catuaba]\n'aba], a Guarani word that means \"what gives strength to the Indian\") is used for the infusions of the bark of a number of trees native to Brazil.\n\n[Guarani language]\nGuarani ( or ), specifically the primary variety known as Paraguayan Guarani (endonym \"avañe'ẽ\" ] 'the people's language'), is an indigenous language of South America that belongs to the Tupi–Guarani family of the Tupian languages.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q9980ed6f2d",
  "kind": "yes/no",
  "text": "Claim: The genus which includes a species of flowering bush commonly known as \"Little Pickles\" has more species in it than Stangeria.\n\nPassages:\n\n[Othonna capensis]\nOthonna capensis also known as Little Pickles, is a species of the genus \"Othonna\" and family Asteraceae and is a native of South Africa.\n\n[Othonna]\nOthonna is a genus of African plants in the sunflower family.\n\n[Stangeria]\nStangeria eriopus is a cycad endemic to southern Africa It is the sole species in the genus Stangeria, most closely related to the Australian genus \"Bowenia\", with which it forms the family Stangeriaceae.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qfbbc33accd",
  "kind": "yes/no",
  "text": "Claim: The Rector of an evangelical Anglican church in the city of Adelaide, South Australia from 1957-1973 was born in Elsternwick, Victoria and died in Melbourne.\n\nPassages:\n\n[Lance Shilton]\nHe was born in late 1921 in Elsternwick, Victoria, a suburb of Melbourne, and educated at the University of Melbourne and ordained in 1950.\n\n[Holy Trinity Church, Adelaide]\nTrinity City (also known as Holy Trinity Church Adelaide, and originally named Trinity Church), is an evangelical Anglican church located at 88 North Terrace, in the city of Adelaide, South Australia.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2e2dce8fae",
  "kind": "yes/no",
  "text": "Claim: Gabriel Gustafson was in charge of the excavation of Oseberg Ship, a well preserved 12th century Viking ship.\n\nPassages:\n\n[Oseberg Ship]\nThe Oseberg ship (Norwegian: \"Osebergskipet\") is a well-preserved Viking ship discovered in a large burial mound at the Oseberg farm near Tønsberg in Vestfold county, Norway.\n\n[Gabriel Gustafson]\nHe was responsible for the excavation and conservation of the Oseberg Ship (\"Osebergfunnet\") .",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qab803daa67",
  "kind": "yes/no",
  "text": "Text: Hear me out... The lyrics in \"coney island\" should've been \"lost again with no surprises, disappointments close your EYESES\" \n\nFixed it for you @taylorswift13 😉\n\n#evermorealbum \n@taylornation13",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 }
]
