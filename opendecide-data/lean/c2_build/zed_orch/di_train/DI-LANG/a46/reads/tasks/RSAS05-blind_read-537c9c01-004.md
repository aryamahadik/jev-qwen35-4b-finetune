# A46 replay label-noise blind read RSAS05-blind_read-537c9c01-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS05-blind_read-537c9c01-004.json

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
  "qid": "q16f448e437",
  "kind": "yes/no",
  "text": "Claim: Bad Moms features an Taiwanese actress, singer-songwriter, and businesswoman who began her career in 1990.\n\nPassages:\n\n[Jada Pinkett Smith]\nJada Koren Pinkett-Smith ( ; née Pinkett; born September 18, 1971) is an American actress, dancer, singer-songwriter, and businesswoman. She began her career in 1990, when she made a guest appearance in the short-lived sitcom \"True Colors\".\n\n[Bad Moms]\nThe film stars an ensemble cast that includes Mila Kunis, Kristen Bell, Kathryn Hahn, Jay Hernandez, Annie Mumolo, Jada Pinkett Smith and Christina Applegate.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q52fb1e761a",
  "kind": "yes/no",
  "text": "Tweet: Efy is great",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qc845fe196a",
  "kind": "yes/no",
  "text": "Claim: Massimiliano Antonio \"Max\" Cavalera played keyboards in the band Soulfly not the artist Gwen Stefani drew inspiration from in her song 4 in the Morning.\n\nPassages:\n\n[4 in the Morning]\nDescribed as one of her favorite songs on the album, Stefani began writing the song while pregnant and finished with Kanal, drawing inspiration from Roberta Flack and Billy Idol.\n\n[Max Cavalera]\nMassimiliano Antonio \"Max\" Cavalera (] , born August 4, 1969) is a Brazilian singer, guitarist, and songwriter who currently plays in heavy metal bands Soulfly, Cavalera Conspiracy, and Killer Be Killed.\n\n[Billy Idol]\nWilliam Michael Albert Broad (born 30 November 1955), known professionally as Billy Idol, is an English musician, singer, songwriter, and actor.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q700a629c71",
  "kind": "yes/no",
  "text": "Claim: R.D. Reid acted in the original version of a movie by director Zack Snyder and featured actor Kevin Zegers, and not the remake by George A. Romero.\n\nPassages:\n\n[Kevin Zegers]\nHe also starred in the films \"Dawn of the Dead\" (2004), \"Transamerica\" (2005), \"It's a Boy Girl Thing\" (2006), \"The Jane Austen Book Club\" (2007), \"Fifty Dead Men Walking\" (2008), and \"Frozen\" (2010).\n\n[R. D. Reid]\nHe appeared in Zack Snyder's \"Dawn of the Dead\", and George A. Romero's \"Diary of the Dead\".\n\n[Dawn of the Dead (2004 film)]\nA remake of George A. Romero's 1978 film of the same name, it was written by James Gunn and stars Sarah Polley, Ving Rhames, Jake Weber, and Mekhi Phifer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe67168d4e7",
  "kind": "yes/no",
  "text": "Claim: The Canadian man whose protege starred in Where Danger Lives had OCD.\n\nPassages:\n\n[Howard Hughes]\nLater in life, he became known for his eccentric behavior and reclusive lifestyle—oddities that were caused in part by a worsening obsessive–compulsive disorder (OCD) and chronic pain from a plane crash.\n\n[Where Danger Lives]\nWhere Danger Lives is a 1950 film noir thriller directed by John Farrow and starring Robert Mitchum, Faith Domergue and Claude Rains. At the time, Domergue was the latest of Howard Hughes' proteges.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qed192a5349",
  "kind": "yes/no",
  "text": "Claim: Parmanand Deepchand Hinduja founded a tech company headquartered in the city of London.\n\nPassages:\n\n[Hinduja Group]\nThe Hinduja Group is an Indian conglomerate company headquartered in London, United Kingdom.\n\n[Parmanand Hinduja]\nParmanand Deepchand Hinduja (1901–1971) was an Indian businessman, the founder of the Hinduja Group.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q3da170959c",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "this time tomorrow i'll be dying at school Cannot Wait!",
   "i am not looking forward to school tomorrow"
  ]
 },
 {
  "qid": "q919ec26ddf",
  "kind": "yes/no",
  "text": "Tweet: @asda just visited your Tamworth store for balloons for my brother’s birthday. Just got them through the door and the 2 has exploded!! https://t.co/NcZ0HGYosI",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q89767ddd19",
  "kind": "yes/no",
  "text": "Claim: Rumours, engineered by Ken Caillat, is the eleventh studio album for the British-American rock band, Fleetwood Mac.\n\nPassages:\n\n[Ken Caillat]\nHe is best known for engineering the Fleetwood Mac albums \"Rumours\", \"Tusk\", \"Mirage\", \"Live\", and \"The Chain Box Set\".\n\n[Rumours (album)]\nRumours is the eleventh studio album by British-American rock band Fleetwood Mac.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qdfd31fcb46",
  "kind": "yes/no",
  "text": "Claim: Brandon Larracuente is known for his role in in the comedy show Bloodline which was produced by Sony Pictures Television.\n\nPassages:\n\n[Bloodline (TV series)]\nBloodline is an American Netflix original thriller–drama web television series created by Todd A. Kessler, Glenn Kessler, and Daniel Zelman, and produced by Sony Pictures Television.\n\n[Brandon Larracuente]\nBrandon Larracuente (born November 16, 1994) is an actor known for his roles in the \"Bloodline\" and \"13 Reasons Why\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q7f517b8187",
  "kind": "yes/no",
  "text": "Claim: Blake LeVine collected an autograph from Brad Pitt, the American actor and producer, born 1963.\n\nPassages:\n\n[Blake LeVine]\nAs a child, he was featured on Entertainment Tonight, Maury Povich, The Jon Stewart Show, CNN, The New York Post, Premiere Magazine, The Los Angeles Times and numerous radio programs about his experiences collecting autographs from celebrities including Princess Diana, Mother Teresa, Brad Pitt, Frank Sinatra and over 1,000 notables.\n\n[Brad Pitt]\nWilliam Bradley Pitt (born December 18, 1963) is an American actor and producer.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe3c522bf20",
  "kind": "yes/no",
  "text": "Claim: Both the poet Maurice Newman and Macquarie University are from Australia.\n\nPassages:\n\n[Maurice Newman]\nMaurice Lionel Newman AC (born 20 April 1938, Ilford, England) is an Australian businessman who has served in a range of public roles, including as Chairperson of the Australian Broadcasting Corporation, chair of the board of the Australian Stock Exchange, Chancellor of Macquarie University, and a member of the Prime Minister's Business Advisory Council from September 2013 to September 2015.\n\n[Macquarie University]\nMacquarie University is a public research university based in Sydney, Australia, in the suburb of Macquarie Park.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q55a86b7aa2",
  "kind": "yes/no",
  "text": "Claim: The publisher Marvel produced the comic books featuring both the family of titles that Maximum Carnage is part of, and the Daredevils.\n\nPassages:\n\n[The Daredevils]\nThe Daredevils was a comics magazine and anthology published by Marvel UK in 1983.\n\n[Maximum Carnage]\nMaximum Carnage is a fourteen-part comic book crossover published in Marvel Comics' \"Spider-Man\" family of titles in 1993.\n\n[Spider-Man]\nSpider-Man is a fictional superhero appearing in American comic books published by Marvel Comics.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q07ef870372",
  "kind": "yes/no",
  "text": "Claim: The creation of Fontana Lake submerged the small town of Proctor, North Carolina and Judson in 1982.\n\nPassages:\n\n[Proctor, North Carolina]\nThe town was flooded by Fontana Lake, which was created by the construction of the Fontana Dam, and remains submerged unless lake levels are very low.\n\n[Fontana Lake]\nMany towns were submerged shortly after the creation of Fontana Lake, such as Proctor and Judson.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q6a721d6b27",
  "kind": "yes/no",
  "text": "Claim: The band Paul Savage was the drummer for is Scottish. They are not the band who released \"Disappointed\".\n\nPassages:\n\n[Disappointed]\n\"Disappointed\" was the fourth single by the English band Electronic.\n\n[Electronic (band)]\nElectronic were an English alternative dance supergroup formed by New Order singer and guitarist Bernard Sumner and ex-Smiths guitarist Johnny Marr.\n\n[Paul Savage]\nPaul Savage is a Scottish musician and record producer, best known for being the drummer in the Scottish indie rock group The Delgados.\n\n[The Delgados]\nThe Delgados were a Scottish indie rock band from Motherwell, North Lanarkshire.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q2cf46b6501",
  "kind": "yes/no",
  "text": "Post: FCAS ✔️",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q11cdcee1a2",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Got a bloody screening invitation for a massive film - YES THAT ONE YOURE THINKING OF - and both screenings are on school days 😭 tempted to quit teaching tbh",
   "I would like to go to the film screening if I could"
  ]
 },
 {
  "qid": "qc4dfae1f68",
  "kind": "yes/no",
  "text": "Claim: Max Domi's father, who was a player for the National Hockey League, was of Albanian origin.\n\nPassages:\n\n[Ontario Raiders]\nMaple Leaf Sports & Entertainment considered purchasing the team, but ultimately a group which included Bill Watters, the then Assistant General Manager of the Toronto Maple Leafs, Paul Beeston, former president of the Toronto Blue Jays, Tie Domi, player for the Maple Leafs, and Bobby Orr, former NHL player, bought it for $250,000 and promptly relocated the team to Toronto's Maple Leaf Gardens where they rebranded it the Toronto Rock.\n\n[Tie Domi]\nTahir \"Tie\" Domi (born November 1, 1969) is a retired Canadian professional ice hockey player of Albanian origin.\n\n[Max Domi]\nHis father is former Toronto Maple Leafs legend Tie Domi.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q67026fef22",
  "kind": "yes/no",
  "text": "Claim: Spike Jonze directed a 2009 fantasy drama film. The star of the slasher film I Am Not a Serial Killer is most notable for his roles as Max in that fantasy drama.\n\nPassages:\n\n[Where the Wild Things Are (film)]\nWhere the Wild Things Are is a 2009 fantasy drama film directed by Spike Jonze.\n\n[Max Records]\nHe is most notable for his roles as Max in the film \"Where the Wild Things Are\", for which he won the 2009 Young Artist Award for Best Leading Young Actor in a Feature Film, and as Slater Pedulla in \"The Sitter\".\n\n[I Am Not a Serial Killer (film)]\nIt stars Christopher Lloyd, Max Records, Laura Fraser, and Christina Baldwin.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q0b2be72ecf",
  "kind": "yes/no",
  "text": "Claim: Marion is approximately 50 miles north of L.A. which is the third-most populous state capital in the U.S.\n\nPassages:\n\n[Marion, Ohio]\nMarion is a city in and the county seat of Marion County, Ohio, United States.\n\n[Columbus, Ohio]\nColumbus ( ) is the capital and largest city of the U.S. state of Ohio. This makes Columbus the third-most populous state capital in the United States, and the second-largest city in the Midwestern United States, after Chicago.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa887b8b076",
  "kind": "yes/no",
  "text": "Tweet: tex-mex restaurants that stop serving breakfast tacos after 10:30/11 am are the reason i have trust issues",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qc3bc3504c8",
  "kind": "yes/no",
  "text": "Claim: A singer has released more solo albums than the singer who Avril Lavigne featured on the song Get Over Me with. This singer co-wrote \"What Were You Thinkin'\"\n\nPassages:\n\n[Get Over Me]\n\"Get Over Me\" is a song by American singer and songwriter Nick Carter featuring Canadian singer Avril Lavigne.\n\n[What Were You Thinkin']\nThe song was written by Porter Howell, Dwayne O'Brien, Brady Seals and Christy DiNapoli.\n\n[Nick Carter (musician)]\nNickolas Gene \"Nick\" Carter (born January 28, 1980) is an American singer, songwriter, actor, and dancer. As of 2015, Carter has released three solo albums, \"Now or Never\", \"I'm Taking Off\" and \"All American\" during breaks between Backstreet Boys schedules, and a collaboration with Jordan Knight titled \"Nick & Knight\".\n\n[Brady Seals]\nBrady Seals (born March 29, 1969) is an American country music artist. A fourth solo album, \"Play Time\", was released in 2009 via Star City.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qb35d4d6586",
  "kind": "yes/no",
  "text": "Tweet: there's something so nice about my iPhone mapping the exact place I took a photo of the holy well I got lost looking for so I can map it onto ArcGIS",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q60e8e20c8d",
  "kind": "yes/no",
  "text": "Claim: George Juskalian took part in the seaborn invasion of French North Africa during WWII.\n\nPassages:\n\n[George Juskalian]\nDuring World War II, he served with the infantry during the North African Campaign and took part in Operation Torch.\n\n[Operation Torch]\nOperation Torch (initially called Operation Gymnast) was the British-United States invasion of French North Africa during the North African Campaign of the Second World War which started on 8 November 1942.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qde54e68fca",
  "kind": "yes/no",
  "text": "Claim: Edsger Wybe Dijkstra (] ; 11 May 1930 – 6 August 2002) was a Dutch computer scientist and an early pioneer in many research areas of computing science who held the Schlumberger Centennial Chair in Computer Sciences at the University of Texas at Austin from 1984 until his retirement in 1999, he was a professor of mathematics (1962–1984) at Eindhoven University of Technology, located in Eindhoven, Netherlands.\n\nPassages:\n\n[Edsger W. Dijkstra]\nHe was a professor of mathematics at the Eindhoven University of Technology (1962–1984) and a research fellow at the Burroughs Corporation (1973–1984).\n\n[Eindhoven University of Technology]\nTU/e ) is a university of technology located in Eindhoven, Netherlands.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q47bbbecc05",
  "kind": "yes/no",
  "text": "Post: yes i have little interest in doing things that applies to me",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q63b3cbd389",
  "kind": "yes/no",
  "text": "Text: FaceTimed with my parents last night while they were with my 6-year-old nephew. I’ve been missing him like crazy worried about being away from him for months, so I asked him if he remembers me. His response?\n“I always will.” ❤️❤️❤️",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q04a2c4803b",
  "kind": "yes/no",
  "text": "Post: can't wait til a bunch of pudgy suburban dads save the day with their firearms",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q30745944fc",
  "kind": "yes/no",
  "text": "Post: Why do I have a doctorate and miss the restaurant industry SO MUCH",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q9df8a62176",
  "kind": "yes/no",
  "text": "Claim: The author of \"The Way the Crow Flies\" had a shorter lifespan than another author. This other author wrote the text for \"Votre Faust\".\n\nPassages:\n\n[The Way the Crow Flies]\nThe Way the Crow Flies is a novel by Canadian writer Ann-Marie MacDonald.\n\n[Michel Butor]\nMichel Butor (] ; 14 September 1926 – 24 August 2016) was a French writer.\n\n[Ann-Marie MacDonald]\nAnn-Marie MacDonald (born October 29, 1958) is a Canadian playwright, novelist, actress and broadcast host who lives in Toronto, Ontario, Canada.\n\n[Votre Faust]\nThe text is by the French author Michel Butor.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q58ed6c6683",
  "kind": "yes/no",
  "text": "Claim: The first solo art exhibition of the author of the book was in 1943. The book inspired the animated film Moomins and the Comet Chase, released in the late 'sixties.\n\nPassages:\n\n[Tove Jansson]\nHer first solo art exhibition was in 1943.\n\n[Moomins and the Comet Chase]\nMoomins and the Comet Chase is a 2010 3D stop motion animated fantasy adventure comedy family film compiled from the \"Comet in Moominland\"-based episodes of the 1977–1982 \"The Moomins\" TV series animated at Se-ma-for in Poland, restored and re-soundtracked with multiple voice actors replacing the single narrator.\n\n[Comet in Moominland]\nComet in Moominland (Swedish: \"Kometjakten\" / \"Mumintrollet på kometjakt\" / \"Kometen kommer\") is the second in Tove Jansson's series of Moomin books.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q376ca9019a",
  "kind": "yes/no",
  "text": "Post: Is only 12 hours away from my first #raceforlife in memory of my grandma - Margaret Jackson who sadly passed away from cancer",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q4992edd89e",
  "kind": "yes/no",
  "text": "Claim: Orontioideae is a subfamily of white flowering plants in the Araceae family. One to two species of skunk cabbage from North America and Asia belong to that subfamily. That subfamily and Ageratum genus are not in the same family.\n\nPassages:\n\n[Orontioideae]\nThe subfamily consists of three genera namely, \"Lysichiton\" (one to two species of skunk cabbage from North America and Asia), \"Orontium\" (golden club, one living species from eastern North America and two extinct species known from fossils), and \"Symplocarpus\" (several species of skunk cabbage from North America and Asia).\n\n[Lysichiton]\nLysichiton is a genus in the family Araceae.\n\n[Ageratum]\nAgeratum ( ), (whiteweed in the USA), is a genus of 40 to 60 tropical and warm temperate flowering annuals and perennials from the family Asteraceae, tribe Eupatorieae.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc426525eca",
  "kind": "yes/no",
  "text": "Post: Good deeds don't go unnoticed 😇",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q6ebf012c09",
  "kind": "yes/no",
  "text": "Claim: Michael Akerfeldt and the Sonic Youth bandmate of Thurston Moore, were guitarists in their respective bands.\n\nPassages:\n\n[Mikael Åkerfeldt]\nLars Mikael Åkerfeldt (born 17 April 1974) is a Swedish musician, prominently known as the lead vocalist, guitarist, and primary songwriter of progressive death metal band Opeth, as well as being the former vocalist of death metal supergroup Bloodbath. He was also guitarist for the \"one-off\" band Steel, and is part of the collaboration Storm Corrosion with Steven Wilson.\n\n[Thurston Moore]\nIn May 2012, \"Spin\" published a staff-selected top 100 ranking Moore and his Sonic Youth bandmate Lee Ranaldo together on number 1.\n\n[Lee Ranaldo]\nLee Mark Ranaldo (born February 3, 1956) is an American musician, singer-songwriter, guitarist, writer, visual artist and record producer, best known as a co-founder of the alternative rock band Sonic Youth. In 2004, \"Rolling Stone\" ranked Ranaldo at number 33 on its \"Greatest Guitarists of All Time\" list.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qdeaecb2b6e",
  "kind": "yes/no",
  "text": "Tweet: @VolphanCarol @littlewhitty @mysticalmanatee I did too, and I also reported Cancun Cruz not worrying about the heartbeats of his constituents without electricity or heat when he fled to Mexico.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qe2da8b5ecb",
  "kind": "yes/no",
  "text": "Post: 2 things I love:\n1. Being woken up by construction work an hour before my alarm.\n2. Sarcasm.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q8f7e20acc7",
  "kind": "yes/no",
  "text": "Claim: The 2003 edition of the game that the 2013 Hawaii Bowl is he eleventh edition of, matched the hometown team with the Houston Cougars. The former coach of the hometown team is now coaching the American team, Hamilton Tiger-Cats.\n\nPassages:\n\n[June Jones]\nJune Sheldon Jones III (born February 19, 1953) is an American football coach and former player, currently serving as a head coach of the Hamilton Tiger-Cats of the Canadian Football League (CFL).\n\n[2003 Hawaii Bowl]\nThe 2003 Sheraton Hawaii Bowl matched the hometown Hawaii Warriors with the Houston Cougars.\n\n[2003 Hawaii Warriors football team]\nThe 2003 Hawaii Warriors football team represented the University of Hawaii at Manoa in the 2003 NCAA Division I-A football season. The Warriors capped off their second straight winning season, and the fourth in five seasons, under head coach June Jones with a bowl win.\n\n[2013 Hawaii Bowl]\nThe twelfth edition of the Hawaii Bowl, it featured the Boise State Broncos from the Mountain West Conference against the Oregon State Beavers from the Pac-12 Conference.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q738fc5c47f",
  "kind": "yes/no",
  "text": "Claim: The later deposed king of England, Scotland and Ireland created The I'Anson Baronetcy of Bassetbury in 1652.\n\nPassages:\n\n[I'Anson baronets]\nThe I'Anson Baronetcy of Bassetbury was a title in the Baronetage of England. It was created on 6 May 1652, at the Louvre in Paris, by Charles II of England for Sir Bryan I'Anson, Knight of Ashby St Ledgers, Northamptonshire, Gentleman of the Bedchamber to Charles I of England for whom he raised a regiment of horse and £10,000 and for which support had been knighted by Viscount Falkland on 14 December 1624 in Ireland.\n\n[Charles II of England]\nCharles II (29 May 1630 – 6 February 1685) was king of England, Scotland and Ireland.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q7d1fc22e32",
  "kind": "yes/no",
  "text": "Claim: This equatorial island is known for Breacachadh which is also known as Breachacha Castle. It is also home to Dùn Dubh.\n\nPassages:\n\n[Coll]\nColl is known for its sandy beaches, which rise to form large sand dunes, for its corncrakes, and for Breacachadh Castle.\n\n[Breachacha Castle]\nBreachacha Castle (also spelled Breacachadh) is either of two structures on the shore of Loch Breachacha, on the Inner Hebridean island of Coll, Scotland.\n\n[Dùn Dubh]\nDùn Dubh is a hillfort, located on the Inner Hebridean island of Coll.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qdf1eea0e9e",
  "kind": "yes/no",
  "text": "Claim: Richard Ira Bong was the famous aviator that died in California while testing a jet aircraft.\n\nPassages:\n\n[R.I. Bong Air Force Base]\nIt was named after the famous aviator, Major Richard Ira Bong, of World War II fame.\n\n[Richard Bong]\nHe died in California while testing a jet aircraft shortly before the Japanese surrendered and the war ended.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q86827c92dd",
  "kind": "yes/no",
  "text": "Claim: The Bourne Ultimatum is the movie which Scott Adkins played a role and is written by Tony Gilroy, Scott Z. Burns and George Nolfi.\n\nPassages:\n\n[The Bourne Ultimatum (film)]\nThe screenplay was written by Tony Gilroy, Scott Z. Burns and George Nolfi and based on a screen story of the novel by Gilroy.\n\n[Scott Adkins]\nHe is also known for playing Bradley Hume in \"Holby City\", Lucian in \"Doctor Strange\", Kiley in \"The Bourne Ultimatum\" and John in \"Zero Dark Thirty\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qfd2d4a8a03",
  "kind": "yes/no",
  "text": "Claim: The actor who played captain hook in the live production with Taylor Louderman won the academy award for his role in The Deer Hunter.\n\nPassages:\n\n[Christopher Walken]\nWalken has received a number of awards and nominations during his career, including winning the Academy Award for Best Supporting Actor for his portrayal of Nikanor \"Nick\" Chebotarevich in \"The Deer Hunter.\"\n\n[Peter Pan Live!]\nThe special featured a live production of the 1954 musical adaptation of \"Peter Pan\", televised from Grumman Studios in Bethpage, New York, starring Allison Williams in the title role and Christopher Walken as Captain Hook.\n\n[Taylor Louderman]\nIn 2013, she appeared as Wendy in NBC's live production of the musical \"Peter Pan\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qb8f2d18470",
  "kind": "yes/no",
  "text": "Claim: An Mandarin rock band released My Animal. This band has more studio albums than The Invisible.\n\nPassages:\n\n[My Animal]\nMy Animal (1998) is the debut album by American rock band Boy Hits Car.\n\n[Boy Hits Car]\nBoy Hits Car released their 5th studio album \"All That Led Us Here\" in May 2014 and are following it up with a European tour.\n\n[The Invisible (band)]\nTheir self-titled debut album, released on 9 March 2009, was nominated for the Mercury Prize and selected as critics choice for iTunes album of the year.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qb37997bb8c",
  "kind": "yes/no",
  "text": "Claim: The second largest convention center on its opening in 1990 is owned by Las Vegas Sands Corporation.\n\nPassages:\n\n[The Palazzo]\nThe hotel and casino are part of a larger complex (operated as one hotel) comprising the adjoining Venetian Resort and Casino and the Sands Convention Center, all of which are owned and operated by the Las Vegas Sands Corporation.\n\n[Sands Expo]\nIt opened in 1990 across the street from the original Sands Hotel, was the second largest convention center in the world when it opened.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qafa26f1ce8",
  "kind": "yes/no",
  "text": "Claim: The European writer of \"Wedding for Disaster\" is the younger brother of one-time Simpsons writer who has also written for the show The Wonder Years.\n\nPassages:\n\n[Joel H. Cohen]\nHe is the younger brother of one-time \"Simpsons\" writer Robert Cohen, who penned the season three episode \"Flaming Moe's.\"\n\n[Wedding for Disaster]\nThe episode was written by Joel H. Cohen and directed by Chuck Sheetz.\n\n[Robert Cohen (writer)]\nHe was raised in Calgary, Alberta and has written for \"The Simpsons\", \"The Wonder Years\", \"The Ben Stiller Show\", \"The Big Bang Theory\", and many other shows.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc1e0533840",
  "kind": "yes/no",
  "text": "Claim: Lee Il-hyung's first feature film was released by Showbox in 1976.\n\nPassages:\n\n[Lee Il-hyung]\nPrior to directing his first feature film \"A Violent Prosecutor\" (2016), Lee is an assistant director on films, such as \"The Moonlight of Seoul\" (2008), \"My Way\" (2011) and \"\" (2014), and commercial films.\n\n[A Violent Prosecutor]\nIt was released in South Korea on February 3, 2016 by Showbox.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q634fd5e2ad",
  "kind": "yes/no",
  "text": "Text: OH MY GOD I AM IN LOVE WITH MY FIANCÉ. https://t.co/LRukiQpXve",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q8b89fbc143",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Eating a bagel with cream cheese cheers me up because it tastes good",
   "ate a bagel with cream cheese earlier and the impending doom immediately vanished from my mind"
  ]
 },
 {
  "qid": "q2f613e3986",
  "kind": "yes/no",
  "text": "Claim: Rockland Railroad Station has been leased to the Class III freight railroad, Central Maine and Quebec Railway, which operates in the U.S. states of Maine and Bath and the Canadian province of Quebec.\n\nPassages:\n\n[Central Maine and Quebec Railway]\nThe Central Maine & Québec Railway (reporting mark CMQ) is a Class III freight railroad operating in the U.S. states of Maine and Vermont and the Canadian province of Quebec with headquarters in New York, NY.\n\n[Rockland Railroad Station]\nThe line has been leased to the Central Maine and Quebec Railway, which is planning to reintroduce service on the line.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 }
]
