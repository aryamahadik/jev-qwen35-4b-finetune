# A46 replay label-noise blind read RSAS07-blind_read-95379c1f-006

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS07-blind_read-95379c1f-006.json

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
  "qid": "q2a3142358f",
  "kind": "yes/no",
  "text": "Claim: The SS-owned company that funded a Nazi association to raise the birth rate of \"Aryan\" children was created in 1942 to market a reflector invented by the chauffeur of Hitler.\n\nPassages:\n\n[Anton Loibl GmbH]\nAnton Loibl GmbH was a company owned by the SS which was a funding source for the Ahnenerbe research branch and the Lebensborn eugenics programme. It was created to market a bicycle reflector invented by Anton Loibl, a chauffeur for Hitler.\n\n[Lebensborn]\nLebensborn e.V. (literally: \"Fount of Life\") was an SS-initiated, state-supported, registered association in Nazi Germany with the goal of raising the birth rate of \"Aryan\" children of persons classified as \"racially pure and healthy\" based on Nazi racial hygiene and health ideology.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf243173a4e",
  "kind": "yes/no",
  "text": "Claim: The Central Harbourfront is a waterfront site it is the result of Central and Wan Chai Reclamation, and it sits to the east of the International Finance Centre (ICC), a skyscraper and an integrated commercial development on the waterfront of the Central District, of Hong Kong.\n\nPassages:\n\n[Central Harbourfront]\nThe Central Harbourfront is a waterfront site in Central, Hong Kong.\n\n[International Finance Centre (Hong Kong)]\nIFC, branded as \"ifc\") is a skyscraper and an integrated commercial development on the waterfront of Hong Kong's Central District.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb7de1d2aea",
  "kind": "yes/no",
  "text": "Claim: MathWorks, an American privately held corporation specializing in mathematical computing software, supports a Professor of Mathematics at Massachusetts Institute of Technology.\n\nPassages:\n\n[Gilbert Strang]\nStrang is the MathWorks Professor of Mathematics at the Massachusetts Institute of Technology.\n\n[MathWorks]\nThe MathWorks, Inc. (branded as simply MathWorks) is an American privately held corporation that specializes in mathematical computing software.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q518e0eb9d5",
  "kind": "yes/no",
  "text": "Claim: The writer of Day of the Iguana worked as a comedian. The director of Scotland Yard (1941 film) did not work as a comedian.\n\nPassages:\n\n[Scotland Yard (1941 film)]\nThe movie was directed by Norman Foster.\n\n[Henry Winkler]\nHenry Franklin Winkler (born October 30, 1945) is an American actor, director, comedian, producer, and author.\n\n[Norman Foster (director)]\nNorman Foster (born Norman Foster Hoeffer, December 13, 1903 – July 7, 1976) was an American actor, film director and screenwriter.\n\n[Day of the Iguana]\nDay of the Iguana is the third book in the Hank Zipzer series by Henry Winkler and Lin Oliver.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q0f46d19d03",
  "kind": "yes/no",
  "text": "Claim: The royal title Marquess of Exeter has been created twice; once in the Peerage of England and once in the Peerage of the United Kingdom did its family own Exeter House.\n\nPassages:\n\n[Exeter House]\nNamed for the Earls of Exeter, whose family owned the property until 1757, the house was notable for the stay of Charles Edward Stuart during the Jacobite Rising of 1745.\n\n[Marquess of Exeter]\nMarquess of Exeter is a title that has been created twice, once in the Peerage of England and once in the Peerage of the United Kingdom.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qc3b6182d53",
  "kind": "yes/no",
  "text": "Claim: Sex Drive is the name of the movie that stars Katrina Bowden and was directed by Sean Anders.\n\nPassages:\n\n[Sex Drive (film)]\nThe film was directed by Sean Anders, and stars Josh Zuckerman, Amanda Crew, Clark Duke, Seth Green, and James Marsden, while Katrina Bowden, Alice Greczyn, Michael Cudlitz, Dave Sheridan, and David Koechner appear in supporting roles.\n\n[Katrina Bowden]\nKatrina Bowden (born September 19, 1988) is an American actress best known for playing Cerie on the NBC sitcom \"30 Rock\" (2006–2013). She also appeared in films such as \"Sex Drive\", \"Piranha 3DD\", and \"Scary Movie 5\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa8f0530965",
  "kind": "yes/no",
  "text": "Claim: Sugata Marjit is the former Vice Chancellor of the University of Calcutta, located in Kolkata (formerly \"Calcutta\"), West Bengal, India established on 24 January 1857.\n\nPassages:\n\n[Sugata Marjit]\nSugata Marjit is the former Vice Chancellor of the University of Calcutta and Reserve Bank of India Professor of Industrial Economics at the Centre for Studies in Social Sciences, Calcutta and the Project Director of Centre for Training & Research in Public Finance and Policy (CTRPFP) [A Ministry of Finance, Government of India funded initiative].\n\n[University of Calcutta]\nThe University of Calcutta (informally known as Calcutta University or CU) is a public state university located in Kolkata (formerly \"Calcutta\"), West Bengal, India established on 24 January 1857.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q4e02b6ae67",
  "kind": "yes/no",
  "text": "Claim: In the 28th season a Spanish rally driver won the racing series which was competed in by Harri Rovanperä from the 1990's to the 2000's.\n\nPassages:\n\n[2000 World Rally Championship]\nThe 2000 World Rally Championship was the 28th season of the FIA World Rally Championship.\n\n[Harri Rovanperä]\nHe drove for SEAT (1997–00), Peugeot (2001–04), Mitsubishi (2005) and Red Bull Škoda Team (2006).\n\n[Carlos Sainz]\nCarlos Sainz Cenamor (born 12 April 1962 in Madrid, Spain) is a Spanish rally driver.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9c01227d72",
  "kind": "yes/no",
  "text": "Claim: The writer and director of Beloved Rogues and David Fincher are both in the film industry.\n\nPassages:\n\n[Alfred Santell]\nAlfred Allen Santell also known as Al Santell (born September 14, 1895 in San Francisco, California) was an American film director and film producer.\n\n[David Fincher]\nDavid Andrew Leo Fincher (born August 28, 1962) is an American director and producer, notably for films, television series and music videos.\n\n[Beloved Rogues]\nBeloved Rogues is a 1917 American silent comedy-drama film directed and written by Alfred Santell with the storyline by Aaron Hoffman.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc6fe79c07f",
  "kind": "yes/no",
  "text": "Claim: The mother of Megan Phelps-Roper is best known as the former spokesperson of a church located in Port Republic.\n\nPassages:\n\n[Megan Phelps-Roper]\nHer mother is Shirley Phelps-Roper, whose father was the church's founder Fred Phelps.\n\n[Shirley Phelps-Roper]\nShe is best known as the former spokesperson of the Westboro Baptist Church of Topeka, Kansas, an organization known for its highly publicized homophobic public protests conducted under the slogan \"God Hates Fags.\"",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q1a8fe802da",
  "kind": "yes/no",
  "text": "Claim: The population in 2010 of the Australian city where Irwin Stadium is located is 2,045.\n\nPassages:\n\n[Oakley High School Stadium]\nThe Oakley High School Stadium, also known as Irwin Stadium, Irwin Field and as KHRI# 109-51, in Oakley, Kansas was built in 1939 by a New Deal works program, the Works Progress Administration (WPA).\n\n[Oakley, Kansas]\nAs of the 2010 census, the city population was 2,045.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q8a77bc7c40",
  "kind": "yes/no",
  "text": "Claim: Catherine Louise Sagal (born January 19, 1954) is an American actress and singer-songwriter, she's know as well for starring in the role of Cate Hennessy, on the show \"8 Simple Rules\", is an American sitcom, originally starring Kurt Sutter as the father.\n\nPassages:\n\n[8 Simple Rules]\n8 Simple Rules (originally 8 Simple Rules for Dating My Teenage Daughter for the first season) is an American sitcom, originally starring John Ritter and Katey Sagal as middle-class parents Paul and Cate Hennessy raising a family of three.\n\n[Katey Sagal]\nShe is best known for her role as Peggy Bundy, Al's sarcastic, lazy, bon bon-eating wife, on \"Married... with Children\" and for her role voicing the character Leela on the animated science-fiction series \"Futurama\" from 1999 to 2003 and 2008 to 2013, as well as for starring on the show \"8 Simple Rules\" in the role of Cate Hennessy.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q70f2979e4d",
  "kind": "yes/no",
  "text": "Claim: Lush and P.O.D. both consist of four band members.\n\nPassages:\n\n[Lush (band)]\nLush were an English rock band formed in London in 1987. The lineup before the original split consisted of Miki Berenyi (vocals, guitar), Emma Anderson (vocals, guitar), Phil King (bass) and Chris Acland (drums).\n\n[P.O.D.]\nPayable on Death (abbreviated P.O.D.) is a Christian nu metal band formed in 1992 and based in San Diego, California. The band's line-up consists of vocalist Sonny Sandoval, drummer Wuv Bernardo, guitarist Marcos Curiel, and bassist Traa Daniels.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q380067f630",
  "kind": "yes/no",
  "text": "Claim: Luiz Felipe Scolari is the FIFA World Cup winner known as Big Phil that Flávio Murtosa works as an assistant coach and manager for.\n\nPassages:\n\n[Luiz Felipe Scolari]\nLuiz Felipe Scolari, (] , ] ; born 9 November 1948), also known as Felipão in Brazil and as Phil Scolari or Big Phil in the English-speaking world, is a FIFA World Cup winner Brazilian football manager and former professional footballer, who is the current manager of Chinese club Guangzhou Evergrande in the Chinese Super League.\n\n[Flávio Murtosa]\nMurtosa has a long friendship with FIFA World Cup winning manager Luiz Felipe Scolari and works mostly as his assistant coach.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q1d1e491c72",
  "kind": "yes/no",
  "text": "Post: Marshalls in Zandvoort be like #WTF1  @MattyWTF1 https://t.co/liviXOQjH7",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q679a32e4e9",
  "kind": "yes/no",
  "text": "Claim: William Hopke played the 1909 Cuban-American Major League Clubs Series, for the Cleveland Indians, the team Erik Sabel played for in 2002, which were founded in 1901.\n\nPassages:\n\n[Erik Sabel]\nHe played for the Arizona Diamondbacks in 1999 and 2001 and the Detroit Tigers in 2002.\n\n[Detroit Tigers]\nOne of the AL's eight charter franchises, the club was founded in Detroit in 1901 .\n\n[Bill Hopke]\nWilliam \"Silent Bill\" Hopke (November 2, 1881 – April 18, 1959) was an American professional baseball player. Hopke also played in the 1909 Cuban-American Major League Clubs Series for the Detroit Tigers, though he never played in a major league game for Detroit.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q29ae7cf463",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "We should have a healthcare system more like the UK which provides free services for all citizens",
   "You guys, how cool would a British version of Breaking Bad be? Lol jk, they have universal health care so Walter White would never have to resort to cooking meth in a trailer to be able to fund his cancer treatment."
  ]
 },
 {
  "qid": "q626959e7d5",
  "kind": "yes/no",
  "text": "Text: i have been informed that, as aroace and agender, i have triple visibility and am now visible from space.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qdbb0ff0d69",
  "kind": "yes/no",
  "text": "Claim: The Basset Bleu de Gascogne and the Beagle are breeds of small hound.\n\nPassages:\n\n[Beagle]\nThe Beagle is a breed of small hound, similar in appearance to the much larger foxhound.\n\n[Basset Bleu de Gascogne]\nThe Basset Bleu de Gascogne (] ), also known as the Blue Gascony Basset, is a long-backed, short legged breed of dog of the hound type.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qfba81d92d0",
  "kind": "yes/no",
  "text": "Claim: Charles Bronson the Actor whose birth name was Charles Dennis Buchinsky, was part of the Leslie Nielsen comedy.\n\nPassages:\n\n[Charles Bronson]\nCharles Bronson (born Charles Dennis Buchinsky; Lithuanian: \"Karolis Dionyzas Bučinskis\" ; November 3, 1921 – August 30, 2003) was an American actor.\n\n[Allan A. Goldstein]\nAllan A. Goldstein (born May 23, 1949) is an American film director and screenwriter, perhaps best known for directing the Charles Bronson vehicle \"\" and the Leslie Nielsen comedy \"\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q509d60c36a",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Day 2348 in lockdown. Never in my life did I think I would utter the words \"I've disinfected the chocolate\". #coronalockdownuk",
   "Day 14 in lockdown."
  ]
 },
 {
  "qid": "q0a1a82d67b",
  "kind": "yes/no",
  "text": "Claim: Andy Cohen is the producer of The Real Housewives of Orange County and also hosts \"Watch What Happens Live with Andy Cohen\".\n\nPassages:\n\n[Andy Cohen (television personality)]\nCohen hosts the Bravo nightly series \"Watch What Happens Live with Andy Cohen\".\n\n[The Real Housewives of Orange County (season 11)]\nIts executive producers are Adam Karpel, Alex Baskin, Douglas Ross, Gregory Stewart, Scott Dunlop, Stephanie Boyriven and Andy Cohen.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q9e4c723c2a",
  "kind": "yes/no",
  "text": "Claim: A mountain near Tomichi Dome was named in honor of an explorer born in the 1800s.\n\nPassages:\n\n[John Williams Gunnison]\nJohn Williams Gunnison (November 11, 1812 – October 26, 1853) was an American military officer and explorer.\n\n[Mount Gunnison]\nThe mountain is named in honor of John Williams Gunnison who explored the area.\n\n[Tomichi Dome]\nOther laccoliths of the Gunnison Country are Mount Crested Butte, Gothic Mountain, Whetstone Mountain, Mount Axtel, Anthracite Range, Round Mountain, Carbon Peak, Beckwith Mountain, Marcellina Mountain and Mount Gunnison.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q57c936d093",
  "kind": "yes/no",
  "text": "Text: I love to pick my modules on a first come first served basis at the same time as everyone in my entire year on a website that hasn’t been updated since 1995 . Thrilling ❤️",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q6c2dcc722c",
  "kind": "yes/no",
  "text": "Claim: Jean Acker was an actor in the film The Ladder of Lies and was born October 23, 1893.\n\nPassages:\n\n[Jean Acker]\nJean Acker (October 23, 1893 – August 16, 1978) was an American film actress with a career dating from the silent film era through the 1950s.\n\n[The Ladder of Lies]\nThe film stars Ethel Clayton, Clyde Fillmore, Jean Acker, Irving Cummings, Charles Meredith and Ruth Ashby.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q46b7dbeedb",
  "kind": "yes/no",
  "text": "Text: Yay for being locked out of your own  house because you forgot your key",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qb341e3ded1",
  "kind": "yes/no",
  "text": "Text: Big day in the Mumford house #sports day",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qe2aa3c5c10",
  "kind": "yes/no",
  "text": "Claim: Total: From Joy Division to New Order is a compilation album of material from Joy Division and English alternative rock band New Order, formed in 1980, currently comprising Bernard Sumner, Stephen Morris, Gillian Gilbert, Phil Cunningham and Tom Chapman.\n\nPassages:\n\n[New Order (band)]\nNew Order are an English rock band formed in 1980, currently comprising Bernard Sumner, Stephen Morris, Gillian Gilbert, Phil Cunningham and Tom Chapman.\n\n[Total: From Joy Division to New Order]\nIt was released in the United Kingdom on 6 June 2011 and is the first album to feature songs from both Joy Division and New Order in one album.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qdcdc667d43",
  "kind": "yes/no",
  "text": "Claim: This lawyer defended the Olympic Park Bomber, an American domestic terrorist convicted for a series of anti-abortion and anti-gay-motivated bombings across the southern United States. She was also the defense attorney in the Trial of Dzhokhar Tsarnaev.\n\nPassages:\n\n[Trial of Dzhokhar Tsarnaev]\nTsarnaev's attorney, Judy Clarke, opened by telling the jurors that her client and his older brother, Tamerlan, planted a bomb killing three and injuring hundreds, as well as murdering a MIT police officer days later.\n\n[Eric Rudolph]\nEric Robert Rudolph (born September 19, 1966), also known as the Olympic Park Bomber, is an American domestic terrorist convicted for a series of anti-abortion and anti-gay-motivated bombings across the southern United States between 1996 and 1998, which killed two people and injured over 120 others.\n\n[Judy Clarke]\nShe has negotiated plea agreements that spare her clients the death penalty, as was the case for Eric Rudolph, Ted Kaczynski, and Jared Lee Loughner.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q1f57416884",
  "kind": "yes/no",
  "text": "Text: what i love about mine and summers work schedules is that she will finish at 8pm and then i’ll start work at 9pm and then when i get home at 7am she’ll start work at 8am ❤️",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q0921678589",
  "kind": "yes/no",
  "text": "Tweet: happy one year vegetarian to me ❤️🌱",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q107d9a8fc2",
  "kind": "yes/no",
  "text": "Claim: The winner of the 2010 Sporting Challenger – Singles was born earlier than the player who defeated Akiko Morigami. This tournament was the 2007 Mirage Cup – Singles.\n\nPassages:\n\n[2010 Sporting Challenger – Singles]\nStarace lost in the final against Simone Bolelli 6–7, 2–6.\n\n[Simone Bolelli]\nSimone Bolelli (born 8 October 1985; ] ) is an Italian professional tennis player.\n\n[2007 Mirage Cup – Singles]\nCaroline Wozniacki defeated Akiko Morigami in the final 6–3, 6–2.\n\n[Caroline Wozniacki]\nCaroline Wozniacki (] , ] ; born 11 July 1990) is a Danish professional tennis player.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q3b2b6d5742",
  "kind": "yes/no",
  "text": "Claim: Alfred A. Marcus worked as a consultant for the utility holding company Xcel Energy Inc.\n\nPassages:\n\n[Alfred A. Marcus]\nHe has worked as a consultant with companies such as 3M, Corning Inc., Xcel Energy, Medtronic, General Mills, and IBM and has also taught as a visiting professor at Technion, INCAE, BI Norwegian Business School, and MIT.\n\n[Xcel Energy]\nXcel Energy Inc. is a utility holding company based in Minneapolis, Minnesota, serving more than 3.3 million electric customers and 1.8 million natural gas customers in Minnesota, Michigan, Wisconsin, North Dakota, South Dakota, Colorado, Texas and New Mexico.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q519e0a91a3",
  "kind": "yes/no",
  "text": "Claim: EasyJet Switzerland the Swiss low-cost commercial airline operated out of the airport that is also connected to by a British express coach operator.\n\nPassages:\n\n[EasyJet Switzerland]\nEasyJet Switzerland SA, styled as easyJet, is a Swiss low-cost airline based in Meyrin, Geneva.\n\n[EasyBus]\nEasyBus is a British express coach operator connecting the city centres of London and Manchester with their respective main airports as well providing services from Geneva Airport (where EasyJet Switzerland is based) to nearby communities.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q6e0eb879b2",
  "kind": "yes/no",
  "text": "Tweet: Also, two whole episodes this season with no D'avin at all. ☹️\n\n#killjoys",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qfe4133b559",
  "kind": "yes/no",
  "text": "Claim: The Union established the advisory board that developed the first ironclad warship in Dover, England.\n\nPassages:\n\n[USS Monitor]\nBuilt during the American Civil War, she was the first ironclad warship commissioned by the Union Navy.\n\n[Ironclad Board]\nThe Ironclad Board was an advisory board established by the Union in 1861 in response to the construction of the \"CSS Virginia\" by the Confederacy during the US Civil War.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q4ee589b410",
  "kind": "yes/no",
  "text": "Claim: Brackenhill Tower is a peel tower, in the parish of Arthuret, Arthuret is a civil parish in the Carlisle district of Cumbria, in England.\n\nPassages:\n\n[Brackenhill Tower]\nBrackenhill Tower is a peel tower, in the parish of Arthuret, in Cumbria, just north of the River Lyne.\n\n[Arthuret]\nArthuret is a civil parish in the Carlisle district of Cumbria, England.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q65deda7597",
  "kind": "yes/no",
  "text": "Claim: A breed the of dog was developed in New London, Wisconsin. That breed was derived before the Estonian Hound.\n\nPassages:\n\n[New London, Wisconsin]\nThe American Water Spaniel was developed as a registered breed by F. J. Pfeifer of New London.\n\n[American Water Spaniel]\nThe breed was saved by Dr. Fred J. Pfeifer, who set up the breed club and standard, and whose work led to recognition for the breed by the United Kennel Club, and later, the American Kennel Club.\n\n[Estonian Hound]\nIt was bred in 1947 when the Soviet Union's national economy ministry decided that every country in the Union must have its own dog breed.\n\n[English Water Spaniel]\nThe English Water Spaniel is a breed of dog that has been extinct since the first part of the 20th century, with the last specimen seen in the 1930s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q69ac0d2a10",
  "kind": "yes/no",
  "text": "Claim: American actor and director Caleb Casey McGuire Affleck-Boldt starred in a 2002 American drama film directed by Gus Van Sant.\n\nPassages:\n\n[Gerry (2002 film)]\nGerry is a 2002 American drama film directed by Gus Van Sant and starring Matt Damon and Casey Affleck, who also co-wrote the film with Van Sant.\n\n[Casey Affleck]\nCaleb Casey McGuire Affleck-Boldt (born August 12, 1975) is an American actor and director.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa66a5eefda",
  "kind": "yes/no",
  "text": "Claim: The airline operating in Whitehorse, Yukon handled 294,000 passengers in 2012.\n\nPassages:\n\n[Erik Nielsen Whitehorse International Airport]\nThe terminal handled 294,000 passengers in 2012, representing a 94% increase in passenger traffic since 2002.\n\n[Air North]\nIts main base is Erik Nielsen Whitehorse International Airport.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4ebdb8fb8c",
  "kind": "yes/no",
  "text": "Claim: Elena Kagan, skewered in \"Newsical\", is an Associate Justice of the Supreme Court of the United States.\n\nPassages:\n\n[Newsical]\nEveryone from President Barack Obama, Lady Gaga, Nancy Grace and Oprah Winfrey to Christina Aguilera, Elena Kagan, Dr.Phill and Sarah Palin are skewered.\n\n[Elena Kagan]\nElena Kagan (pronounced ; born April 28, 1960) is an Associate Justice of the Supreme Court of the United States.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q20b9348e65",
  "kind": "yes/no",
  "text": "Claim: The award-winning actor Thomas Gregory played in a drama television series based on Israeli series the \"Yellow Peppers\".\n\nPassages:\n\n[The A Word]\nThe A Word is a BBC drama television series based on Israeli series the \"Yellow Peppers\" (פלפלים צהובים) by Keren Margalit.\n\n[Thomas Gregory (actor)]\nThomas Gregory (born 10 November 1995) is an English actor who played Luke Taylor in BBC One drama \"The A Word\", first broadcast in March 2016.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q80d5bf98cf",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I would say \"bonding with the jsc homies\".",
   "💫jsc bonding nights💫🥰🥳"
  ]
 },
 {
  "qid": "q08be4cde97",
  "kind": "yes/no",
  "text": "Claim: The Bollywood studio's You're Not You's 2017 film release is a 3D computer-animated comedy.\n\nPassages:\n\n[You're Not You]\nYou're Not You is a 2014 American drama film directed by George C. Wolfe and written by Jordan Roberts and Shana Feste, based on a novel of the same name by Michelle Wildgen.\n\n[Jordan Roberts (writer)]\nJordan Roberts (born Bruce Robert Jordan; June 19, 1957) is an American screenwriter and film director, known for co-writing the screenplays for the Academy Award-winning animated Disney film \"Big Hero 6\" (2014), for which he was nominated for the Annie Award for Writing in a Feature Production and \"Ferdinand\" (2017).\n\n[Ferdinand (film)]\nFerdinand is an upcoming 2017 American 3D computer-animated comedy film produced by Blue Sky Studios and 20th Century Fox Animation.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q17552329d9",
  "kind": "yes/no",
  "text": "Text: Only a a President as strong and decisive as @realDonaldTrump would force the FDA to OK a drug even before clinical trial results are in.  No need to wait for such silly formalities - people have been taking the drug for years and most are still alive and fine! #OkToTry #Gotrump https://t.co/IdxTJ7kucp",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qad4620bdbc",
  "kind": "yes/no",
  "text": "Tweet: don't cry because it happened, smile because it's over &lt;3",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qeb1cf5a985",
  "kind": "yes/no",
  "text": "Claim: Peggy Trentini made her acting debut in the 1982 film. \"Leni\" Riefenstahl was born before the director of the film.\n\nPassages:\n\n[Garry Marshall]\nGarry Kent Marshall (November 13, 1934 – July 19, 2016) was an American actor, director, producer, writer, and voice artist best known for creating \"Happy Days\" and its various spin-offs, developing Neil Simon's 1965 play \"The Odd Couple\" for television, and directing \"Pretty Woman\", \"Runaway Bride\", \"Valentine's Day\", \"New Year's Eve\", \"Mother's Day\", \"\"The Princess Diaries\", and \"\".\n\n[Young Doctors in Love]\nYoung Doctors in Love is a 1982 American comedy film directed by Garry Marshall.\n\n[Leni Riefenstahl]\nHelene Bertha Amalie \"Leni\" Riefenstahl (] ; 22 August 1902 – 8 September 2003) was a German film director, producer, screenwriter, editor, photographer, actress and dancer.\n\n[Peggy Trentini]\nTrentini made her film debut in 1982 with a small part in the comedy movie \"Young Doctors in Love\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qc86e9513da",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "So I have an exam tomorrow, but likeee if the country is about to turn into a war zone does it really matter??",
   "I have to take this exam even when the world is falling apart."
  ]
 },
 {
  "qid": "qd82d64e356",
  "kind": "yes/no",
  "text": "Post: wearing a cute jumpsuit is all fun and games until you have to go to the bathroom",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q513104e2d7",
  "kind": "yes/no",
  "text": "Claim: 15 March 1983 is the birth date of the star of Igualita a mí named Adrian Suar.\n\nPassages:\n\n[Igualita a mí]\nIgualita a mí is a 2010 Argentine comedy film directed by Diego Kaplan and starring Florencia Bertotti and Adrián Suar.\n\n[Florencia Bertotti]\nMaría Florencia Bertotti ] ; (born 15 March 1983), better known as Florencia Bertotti, is an Argentine actress, singer and producer.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 }
]
